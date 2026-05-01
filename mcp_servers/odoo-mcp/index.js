#!/usr/bin/env node

/**
 * Odoo MCP Server
 *
 * Integrates Claude with Odoo Community Edition via JSON-RPC API
 * Allows Claude to:
 * - Create/read/update invoices (draft status)
 * - Record transactions and expenses
 * - Query customer accounts
 * - Generate financial reports
 * - List unpaid invoices
 *
 * All financial operations start as DRAFT
 * Posting requires human approval via HITL workflow
 */

const express = require('express');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(express.json());

// Configuration
const ODOO_URL = process.env.ODOO_URL || 'http://localhost:8069';
const ODOO_DB = process.env.ODOO_DB || 'hackathon0_business';
const ODOO_UID = process.env.ODOO_UID || 2; // Admin user
const ODOO_PASSWORD = process.env.ODOO_PASSWORD || 'admin';
const MCP_PORT = process.env.MCP_PORT || 3001;

// Odoo XML-RPC Client
class OdooClient {
  constructor(url, db, uid, password) {
    this.url = url;
    this.db = db;
    this.uid = uid;
    this.password = password;
    this.session_id = null;
  }

  async authenticate() {
    try {
      const response = await axios.post(`${this.url}/web/session/authenticate`, {
        jsonrpc: '2.0',
        method: 'call',
        params: {
          db: this.db,
          login: 'admin',
          password: this.password
        }
      });

      if (response.data.result) {
        this.session_id = response.data.result.session_id;
        console.log('✓ Odoo authentication successful');
        return true;
      }
    } catch (error) {
      console.error('✗ Odoo authentication failed:', error.message);
      return false;
    }
  }

  async call(model, method, args = [], kwargs = {}) {
    try {
      const response = await axios.post(`${this.url}/web/dataset/call_kw/${model}/${method}`, {
        jsonrpc: '2.0',
        method: 'call',
        params: {
          model: model,
          method: method,
          args: args,
          kwargs: kwargs
        }
      }, {
        headers: {
          'Cookie': `session_id=${this.session_id}`
        }
      });

      return response.data.result;
    } catch (error) {
      throw new Error(`Odoo API error: ${error.message}`);
    }
  }

  // Invoice operations
  async createInvoice(customer_id, amount, description) {
    try {
      const invoice_data = {
        partner_id: customer_id,
        move_type: 'out_invoice',
        invoice_date: new Date().toISOString().split('T')[0],
        state: 'draft',
        invoice_line_ids: [[0, 0, {
          name: description,
          quantity: 1,
          price_unit: amount,
          account_id: 1 // Default sales account
        }]]
      };

      const result = await this.call('account.move', 'create', [invoice_data]);
      return {
        success: true,
        invoice_id: result,
        status: 'draft',
        note: 'Invoice created in DRAFT status. Requires approval before posting.'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getInvoice(invoice_id) {
    try {
      const result = await this.call('account.move', 'read', [
        [invoice_id],
        ['id', 'name', 'partner_id', 'amount_total', 'state', 'invoice_date']
      ]);
      return result[0] || null;
    } catch (error) {
      return null;
    }
  }

  async listUnpaidInvoices() {
    try {
      const result = await this.call('account.move', 'search_read', [
        [['move_type', '=', 'out_invoice'], ['payment_state', '!=', 'paid']],
        ['id', 'name', 'partner_id', 'amount_total', 'invoice_date']
      ]);
      return result;
    } catch (error) {
      return [];
    }
  }

  async recordTransaction(account_id, amount, description) {
    try {
      const journal_entry = {
        ref: description,
        date: new Date().toISOString().split('T')[0],
        line_ids: [[0, 0, {
          account_id: account_id,
          debit: amount > 0 ? amount : 0,
          credit: amount < 0 ? -amount : 0,
          name: description
        }]]
      };

      const result = await this.call('account.move', 'create', [journal_entry]);
      return {
        success: true,
        transaction_id: result
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getCustomerStatus(customer_name) {
    try {
      const partners = await this.call('res.partner', 'search_read', [
        [['name', 'ilike', customer_name]],
        ['id', 'name', 'email', 'phone']
      ]);

      if (partners.length === 0) return null;

      const partner = partners[0];
      const invoices = await this.call('account.move', 'search_read', [
        [['partner_id', '=', partner.id], ['move_type', '=', 'out_invoice']],
        ['id', 'name', 'amount_total', 'payment_state']
      ]);

      const balance = invoices.reduce((sum, inv) => {
        return sum + (inv.payment_state === 'paid' ? 0 : inv.amount_total);
      }, 0);

      return {
        customer_id: partner.id,
        name: partner.name,
        email: partner.email,
        phone: partner.phone,
        outstanding_balance: balance,
        invoice_count: invoices.length,
        invoices: invoices
      };
    } catch (error) {
      return null;
    }
  }

  async getSummary() {
    try {
      const invoices = await this.call('account.move', 'search_read', [
        [['move_type', '=', 'out_invoice']],
        ['id', 'amount_total', 'payment_state']
      ]);

      const total_revenue = invoices.reduce((sum, inv) => sum + inv.amount_total, 0);
      const unpaid = invoices.filter(inv => inv.payment_state !== 'paid').length;

      return {
        total_invoices: invoices.length,
        total_revenue: total_revenue,
        unpaid_count: unpaid,
        last_updated: new Date().toISOString()
      };
    } catch (error) {
      return { error: error.message };
    }
  }
}

// Initialize Odoo client
const odooClient = new OdooClient(ODOO_URL, ODOO_DB, ODOO_UID, ODOO_PASSWORD);

// ============= MCP ENDPOINTS =============

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'odoo-mcp' });
});

// Authentication
app.post('/authenticate', async (req, res) => {
  const success = await odooClient.authenticate();
  res.json({ authenticated: success });
});

// Create Invoice
app.post('/invoice/create', async (req, res) => {
  const { customer_id, amount, description } = req.body;

  if (!customer_id || !amount || !description) {
    return res.status(400).json({
      error: 'Missing required fields: customer_id, amount, description'
    });
  }

  const result = await odooClient.createInvoice(customer_id, amount, description);
  res.json(result);
});

// Get Invoice
app.get('/invoice/:id', async (req, res) => {
  const invoice = await odooClient.getInvoice(req.params.id);
  res.json(invoice || { error: 'Invoice not found' });
});

// List Unpaid Invoices
app.get('/invoices/unpaid', async (req, res) => {
  const invoices = await odooClient.listUnpaidInvoices();
  res.json({ unpaid_invoices: invoices, count: invoices.length });
});

// Record Transaction
app.post('/transaction/record', async (req, res) => {
  const { account_id, amount, description } = req.body;

  if (!account_id || !amount || !description) {
    return res.status(400).json({
      error: 'Missing required fields: account_id, amount, description'
    });
  }

  const result = await odooClient.recordTransaction(account_id, amount, description);
  res.json(result);
});

// Get Customer Status
app.get('/customer/:name', async (req, res) => {
  const status = await odooClient.getCustomerStatus(req.params.name);
  res.json(status || { error: 'Customer not found' });
});

// Get Financial Summary
app.get('/summary', async (req, res) => {
  const summary = await odooClient.getSummary();
  res.json(summary);
});

// ============= STARTUP =============

async function startup() {
  console.log('Starting Odoo MCP Server...');
  console.log(`Odoo URL: ${ODOO_URL}`);
  console.log(`Database: ${ODOO_DB}`);

  // Try to authenticate
  const authenticated = await odooClient.authenticate();

  if (!authenticated) {
    console.warn('⚠️  Could not authenticate with Odoo. Make sure Odoo is running.');
    console.warn(`URL: ${ODOO_URL}`);
  }

  // Start server
  app.listen(MCP_PORT, () => {
    console.log(`✓ Odoo MCP Server listening on port ${MCP_PORT}`);
    console.log(`  Endpoints:`);
    console.log(`  POST   /authenticate                - Authenticate with Odoo`);
    console.log(`  POST   /invoice/create              - Create invoice (draft)`);
    console.log(`  GET    /invoice/:id                 - Get invoice details`);
    console.log(`  GET    /invoices/unpaid             - List unpaid invoices`);
    console.log(`  POST   /transaction/record          - Record transaction`);
    console.log(`  GET    /customer/:name              - Get customer status`);
    console.log(`  GET    /summary                     - Get financial summary`);
  });
}

startup().catch(console.error);
