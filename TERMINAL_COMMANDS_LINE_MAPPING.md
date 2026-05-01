---
title: Terminal Commands - Complete Line Number Mapping
date: 2026-03-30
version: 2.0
status: COMPLETE
---

# Terminal Commands: Complete Line Number Mapping

## ALL 6 TEST GUIDES - Terminal Commands Listed by Line Number

This document provides the exact line numbers where each terminal command appears in all 6 enhanced test guides.

---

## 📱 FACEBOOK TEST GUIDE (804 lines total)

### Test 1: Basic Facebook Post Creation
- **Line 28**: `cd /path/to/project`
- **Line 31**: `pwd`
- **Line 37**: `python scripts/trigger_posts.py -p facebook -c "Great news from our team!" --preview`
- **Line 69**: `ls Pending_Approval/ | grep "POST_.*_fac_"`
- **Line 78**: `cat Pending_Approval/POST_20260329_101534_fac_abc123.md`

### Test 2: Facebook Default Content
- **Line 106**: `python scripts/trigger_posts.py -p facebook --preview`
- **Line 143**: `cat Pending_Approval/POST_20260329_101600_fac_xyz789.md`

### Test 3: Facebook Orchestrator Detection
- **Line 168**: `python scripts/master_orchestrator.py`
- **Line 188**: `python scripts/trigger_posts.py -p facebook -c "Testing orchestrator detection"`
- **Line 200**: `ls Pending_Approval/ | grep "_fac_"`
- **Line 205**: `mv Pending_Approval/POST_20260329_101534_fac_test1.md Approved/`
- **Line 208**: `ls Approved/ | grep "_fac_"`
- **Line 212**: `ls Pending_Approval/ | grep "_fac_" | wc -l`

### Test 4: Facebook Executor Processing
- **Line 261**: `ls Done/ | grep "_fac_"`
- **Line 266**: `ls Approved/ | grep "_fac_" | wc -l`
- **Line 273**: `grep "fac_test1" Logs/orchestrator_*.log`

### Test 5: Facebook Batch Processing
- **Line 301**: `python scripts/trigger_posts.py -p facebook -c "Post 1: First update" -t "Post 1"`
- **Line 302**: `sleep 10`
- **Line 305**: `python scripts/trigger_posts.py -p facebook -c "Post 2: Second update" -t "Post 2"`
- **Line 306**: `sleep 10`
- **Line 309**: `python scripts/trigger_posts.py -p facebook -c "Post 3: Third update" -t "Post 3"`
- **Line 312**: `ls Pending_Approval/ | grep "_fac_" | wc -l`
- **Line 319**: `mv Pending_Approval/POST_*_fac_*.md Approved/`
- **Line 322**: `ls Approved/ | grep "_fac_" | wc -l`
- **Line 326**: `ls Pending_Approval/ | grep "_fac_" | wc -l`
- **Line 353**: `ls Done/ | grep "_fac_" | wc -l`
- **Line 357**: `ls Approved/ | grep "_fac_" | wc -l`
- **Line 361**: `echo "Total posts in Done:"`
- **Line 362**: `ls Done/ | grep "_fac_" | wc -l`
- **Line 363**: `echo "Total posts in Approved:"`
- **Line 364**: `ls Approved/ | grep "_fac_" | wc -l`

### Test 6: Facebook Error Recovery
- **Line 388**: `python scripts/trigger_posts.py -p facebook -c "Error recovery test"`
- **Line 393**: `mv Pending_Approval/POST_*_fac_*.md Approved/`

### Test 7: Facebook Content with Special Characters
- **Line 451-452**: `python scripts/trigger_posts.py -p facebook -c "Check this out! 🎉 #Facebook @friends \"See the post\"" --preview`
- **Line 465**: `cat Pending_Approval/POST_*_fac_*.md`
- **Line 478**: `grep "🎉" Pending_Approval/POST_*_fac_*.md`
- **Line 482**: `grep "#Facebook" Pending_Approval/POST_*_fac_*.md`
- **Line 486**: `grep "@friends" Pending_Approval/POST_*_fac_*.md`
- **Line 490**: `grep '"See the post"' Pending_Approval/POST_*_fac_*.md`
- **Line 497**: `mv Pending_Approval/POST_*_fac_*.md Approved/`

### Test 8: Facebook Session Persistence
- **Line 528**: `python scripts/trigger_posts.py -p facebook -c "Post 1"`
- **Line 529**: `mv Pending_Approval/POST_*_fac_001.md Approved/`
- **Line 551**: `python scripts/trigger_posts.py -p facebook -c "Post 2"`
- **Line 552**: `mv Pending_Approval/POST_*_fac_002.md Approved/`
- **Line 570**: `ls -la session/`
- **Line 582**: `python scripts/trigger_posts.py -p facebook -c "Post 3"`
- **Line 583**: `mv Pending_Approval/POST_*_fac_003.md Approved/`

### Test 9: Facebook Performance Timing
- **Line 610**: `date "+%H:%M:%S"`
- **Line 613**: `python scripts/trigger_posts.py -p facebook -c "Performance test"`
- **Line 619**: `date "+%H:%M:%S"`
- **Line 622**: `mv Pending_Approval/POST_*_fac_*.md Approved/`
- **Line 642**: `grep "POST_*_fac" Logs/orchestrator_*.log | head -20`

### Test 10: Facebook HITL Workflow
- **Line 669**: `python scripts/trigger_posts.py -p facebook -c "New announcement for everyone!"`
- **Line 677**: `cat Pending_Approval/POST_*_fac_hitl.md`
- **Line 691**: `mv Pending_Approval/POST_*_fac_hitl.md Approved/`
- **Line 710**: `ls Done/ | grep "_fac_hitl"`
- **Line 714**: `ls Approved/ | grep "_fac_hitl" | wc -l`

### Troubleshooting Section
- **Line 737**: `playwright install firefox chromium`
- **Line 740**: `lsof -i :9999`
- **Line 743**: `pkill -f social_media_executor`
- **Line 750**: `ps aux | grep master_orchestrator`
- **Line 753**: `python scripts/master_orchestrator.py`
- **Line 756**: `tail -20 Logs/orchestrator_*.log`
- **Line 762**: `ls -la | grep -E "Pending_Approval|Approved|Done"`
- **Line 765**: `mkdir -p Pending_Approval Approved Done Logs session`
- **Line 768**: `chmod 755 Pending_Approval Approved Done`
- **Line 774**: `ls -la session/`
- **Line 778**: `rm -rf session/*`

---

## 🐦 TWITTER TEST GUIDE (578 lines total)

### Test 1: Basic Twitter Post Creation
- **Line 23**: `cd /path/to/project`
- **Line 26**: `python scripts/trigger_posts.py -p twitter -c "Just launched something amazing! 🚀" --preview`
- **Line 57**: `ls Pending_Approval/ | grep "_tw_"`
- **Line 64**: `cat Pending_Approval/POST_20260329_101534_tw_xyz123.md`

### Test 2: Twitter Default Content
- **Line 88**: `python scripts/trigger_posts.py -p twitter --preview`
- **Line 113**: `cat Pending_Approval/POST_20260329_101600_tw_abc789.md | grep -A 10 "# Twitter Post"`

### Test 3: Twitter Orchestrator Detection
- **Line 141**: `python scripts/master_orchestrator.py`
- **Line 153**: `python scripts/trigger_posts.py -p twitter -c "Testing detection"`
- **Line 158**: `mv Pending_Approval/POST_*_tw_*.md Approved/`

### Test 4: Twitter Executor Processing
- **Line 199**: `ls Done/ | grep "_tw_"`
- **Line 204**: `ls Approved/ | grep "_tw_" | wc -l`

### Test 5: Twitter Character Limit Check
- **Line 231-232**: `python scripts/trigger_posts.py -p twitter -c "This is a test tweet with content..."`
- **Line 241-242**: `python scripts/trigger_posts.py -p twitter -c "This is a very long test tweet..."`
- **Line 250**: `mv Pending_Approval/POST_*_tw_*.md Approved/`

### Test 6: Twitter Performance Timing
- **Line 275**: `date "+%H:%M:%S"`
- **Line 278**: `python scripts/trigger_posts.py -p twitter -c "Perf test"`
- **Line 284**: `date "+%H:%M:%S"`
- **Line 287**: `mv Pending_Approval/POST_*_tw_*.md Approved/`

### Test 7: Twitter Batch Processing
- **Line 320**: `python scripts/trigger_posts.py -p twitter -c "Tweet 1: First" && sleep 10`
- **Line 323**: `python scripts/trigger_posts.py -p twitter -c "Tweet 2: Second" && sleep 10`
- **Line 326**: `python scripts/trigger_posts.py -p twitter -c "Tweet 3: Third" && sleep 10`
- **Line 329**: `python scripts/trigger_posts.py -p twitter -c "Tweet 4: Fourth" && sleep 10`
- **Line 332**: `python scripts/trigger_posts.py -p twitter -c "Tweet 5: Fifth"`
- **Line 335**: `ls Pending_Approval/ | grep "_tw_" | wc -l`
- **Line 342**: `mv Pending_Approval/POST_*_tw_*.md Approved/`
- **Line 345**: `ls Approved/ | grep "_tw_" | wc -l`
- **Line 364**: `ls Done/ | grep "_tw_" | wc -l`
- **Line 368**: `ls Approved/ | grep "_tw_" | wc -l`

### Test 8: Twitter Error Recovery
- **Line 393**: `python scripts/trigger_posts.py -p twitter -c "Error test tweet"`
- **Line 394**: `mv Pending_Approval/POST_*_tw_*.md Approved/`

### Test 9: Twitter Special Characters
- **Line 433-434**: `python scripts/trigger_posts.py -p twitter -c "Test 🚀 #hashtag @mention \"quoted text\"" --preview`
- **Line 440**: `cat Pending_Approval/POST_*_tw_*.md | grep -i "test"`
- **Line 447**: `mv Pending_Approval/POST_*_tw_*.md Approved/`

### Test 10: Twitter Session Persistence
- **Line 473**: `python scripts/trigger_posts.py -p twitter -c "Tweet 1"`
- **Line 474**: `mv Pending_Approval/POST_*_tw_001.md Approved/`
- **Line 487**: `python scripts/trigger_posts.py -p twitter -c "Tweet 2"`
- **Line 488**: `mv Pending_Approval/POST_*_tw_002.md Approved/`
- **Line 500**: `python scripts/trigger_posts.py -p twitter -c "Tweet 3"`
- **Line 501**: `mv Pending_Approval/POST_*_tw_003.md Approved/`
- **Line 513**: `ls -la session/`

### Troubleshooting Section
- **Line 533**: `playwright install chromium firefox`
- **Line 534**: `pkill -f social_media_executor`
- **Line 536**: `python scripts/master_orchestrator.py`
- **Line 541**: `ps aux | grep master_orchestrator`
- **Line 546**: `tail -20 Logs/orchestrator_*.log`
- **Line 552**: `mkdir -p Pending_Approval Approved Done Logs session`
- **Line 555**: `chmod 755 Pending_Approval Approved Done`

---

## 📷 INSTAGRAM TEST GUIDE (510 lines total)

### Test 1: Basic Instagram Post Creation
- **Line 22**: `cd /path/to/project`
- **Line 24**: `python scripts/trigger_posts.py -p instagram -c "Creating something beautiful ✨" --preview`
- **Line 54**: `ls Pending_Approval/ | grep "_ig_"`
- **Line 57**: `cat Pending_Approval/POST_20260329_101534_ig_abc123.md`

### Test 2: Instagram Default Content
- **Line 80**: `python scripts/trigger_posts.py -p instagram --preview`
- **Line 101**: `cat Pending_Approval/POST_*_ig_*.md | grep -A 10 "# Instagram Post"`

### Test 3: Instagram Orchestrator Detection
- **Line 123**: `python scripts/master_orchestrator.py`
- **Line 128**: `python scripts/trigger_posts.py -p instagram -c "Test post for detection"`
- **Line 133**: `mv Pending_Approval/POST_*_ig_*.md Approved/`

### Test 4: Instagram Executor Processing
- **Line 172**: `ls Done/ | grep "_ig_"`
- **Line 175**: `ls Approved/ | grep "_ig_" | wc -l`

### Test 5: Instagram Visual Content & Emojis
- **Line 200-201**: `python scripts/trigger_posts.py -p instagram -c "Beautiful capture 📸 Amazing moment 🌟 Love this 💕 Nature 🌿" --preview`
- **Line 207**: `cat Pending_Approval/POST_*_ig_*.md | grep -o "📸\|🌟\|💕\|🌿"`
- **Line 218**: `mv Pending_Approval/POST_*_ig_*.md Approved/`

### Test 6: Instagram Performance Timing
- **Line 242**: `date "+%H:%M:%S"`
- **Line 243**: `python scripts/trigger_posts.py -p instagram -c "Perf test"`
- **Line 249**: `date "+%H:%M:%S"`
- **Line 250**: `mv Pending_Approval/POST_*_ig_*.md Approved/`

### Test 7: Instagram Batch Processing
- **Line 281**: `python scripts/trigger_posts.py -p instagram -c "Post 1: First" && sleep 10`
- **Line 282**: `python scripts/trigger_posts.py -p instagram -c "Post 2: Second" && sleep 10`
- **Line 283**: `python scripts/trigger_posts.py -p instagram -c "Post 3: Third" && sleep 10`
- **Line 284**: `python scripts/trigger_posts.py -p instagram -c "Post 4: Fourth"`
- **Line 287**: `ls Pending_Approval/ | grep "_ig_" | wc -l`
- **Line 293**: `mv Pending_Approval/POST_*_ig_*.md Approved/`
- **Line 295**: `ls Approved/ | grep "_ig_" | wc -l`
- **Line 311**: `ls Done/ | grep "_ig_" | wc -l`
- **Line 314**: `ls Approved/ | grep "_ig_" | wc -l`

### Test 8: Instagram Error Recovery
- **Line 337**: `python scripts/trigger_posts.py -p instagram -c "Error test"`
- **Line 338**: `mv Pending_Approval/POST_*_ig_*.md Approved/`

### Test 9: Instagram Caption Formatting
- **Line 373-374**: `python scripts/trigger_posts.py -p instagram -c "Amazing shot 📸 #instagram @friends \"Love this\"" --preview`
- **Line 380**: `cat Pending_Approval/POST_*_ig_*.md | grep -A 5 "# Instagram"`
- **Line 387**: `mv Pending_Approval/POST_*_ig_*.md Approved/`

### Test 10: Instagram Session Persistence
- **Line 412**: `python scripts/trigger_posts.py -p instagram -c "Post 1"`
- **Line 413**: `mv Pending_Approval/POST_*_ig_001.md Approved/`
- **Line 426**: `python scripts/trigger_posts.py -p instagram -c "Post 2"`
- **Line 427**: `mv Pending_Approval/POST_*_ig_002.md Approved/`
- **Line 439**: `python scripts/trigger_posts.py -p instagram -c "Post 3"`
- **Line 440**: `mv Pending_Approval/POST_*_ig_003.md Approved/`
- **Line 452**: `ls -la session/`

### Troubleshooting Section
- **Line 471**: `playwright install chromium`
- **Line 472**: `pkill -f social_media_executor`
- **Line 473**: `python scripts/master_orchestrator.py`
- **Line 478**: `ps aux | grep master_orchestrator`
- **Line 481**: `tail -20 Logs/orchestrator_*.log`
- **Line 486**: `mkdir -p Pending_Approval Approved Done Logs session`
- **Line 487**: `chmod 755 Pending_Approval Approved Done`

---

## 💬 WHATSAPP TEST GUIDE (527 lines total)

### Test 1: Basic WhatsApp Message Creation
- **Line 22**: `cd /path/to/project`
- **Line 24**: `python scripts/trigger_posts.py -p whatsapp -c "Hey! Just wanted to reach out." --preview`
- **Line 54**: `ls Pending_Approval/ | grep "_wa_"`
- **Line 57**: `cat Pending_Approval/POST_20260329_101534_wa_xyz123.md`

### Test 2: WhatsApp Default Content
- **Line 80**: `python scripts/trigger_posts.py -p whatsapp --preview`
- **Line 97**: `cat Pending_Approval/POST_*_wa_*.md | grep -A 5 "# WhatsApp"`

### Test 3: WhatsApp Orchestrator Detection
- **Line 121**: `python scripts/master_orchestrator.py`
- **Line 126**: `python scripts/trigger_posts.py -p whatsapp -c "Testing detection"`
- **Line 131**: `mv Pending_Approval/POST_*_wa_*.md Approved/`

### Test 4: WhatsApp Executor Processing
- **Line 170**: `ls Done/ | grep "_wa_"`
- **Line 173**: `ls Approved/ | grep "_wa_" | wc -l`

### Test 5: WhatsApp Message Formatting
- **Line 198-203**: `python scripts/trigger_posts.py -p whatsapp -c "First line of message.\nSecond line here.\nThird line!\n\nFinal paragraph." --preview`
- **Line 209**: `cat Pending_Approval/POST_*_wa_*.md | grep -A 10 "# WhatsApp"`
- **Line 216**: `mv Pending_Approval/POST_*_wa_*.md Approved/`

### Test 6: WhatsApp Performance Timing
- **Line 241**: `date "+%H:%M:%S"`
- **Line 242**: `python scripts/trigger_posts.py -p whatsapp -c "Perf test"`
- **Line 248**: `date "+%H:%M:%S"`
- **Line 249**: `mv Pending_Approval/POST_*_wa_*.md Approved/`

### Test 7: WhatsApp Batch Processing
- **Line 281**: `python scripts/trigger_posts.py -p whatsapp -c "Message 1" && sleep 10`
- **Line 282**: `python scripts/trigger_posts.py -p whatsapp -c "Message 2" && sleep 10`
- **Line 283**: `python scripts/trigger_posts.py -p whatsapp -c "Message 3"`
- **Line 286**: `ls Pending_Approval/ | grep "_wa_" | wc -l`
- **Line 292**: `mv Pending_Approval/POST_*_wa_*.md Approved/`
- **Line 294**: `ls Approved/ | grep "_wa_" | wc -l`
- **Line 309**: `ls Done/ | grep "_wa_" | wc -l`
- **Line 312**: `ls Approved/ | grep "_wa_" | wc -l`

### Test 8: WhatsApp Error Recovery
- **Line 336**: `python scripts/trigger_posts.py -p whatsapp -c "Error test"`
- **Line 337**: `mv Pending_Approval/POST_*_wa_*.md Approved/`

### Test 9: WhatsApp Emoji Support
- **Line 377-378**: `python scripts/trigger_posts.py -p whatsapp -c "Hello! 👋 Great to see you! 😊 How are things? 🌟" --preview`
- **Line 384**: `cat Pending_Approval/POST_*_wa_*.md | grep -o "👋\|😊\|🌟"`
- **Line 394**: `mv Pending_Approval/POST_*_wa_*.md Approved/`

### Test 10: WhatsApp Session Persistence
- **Line 419**: `python scripts/trigger_posts.py -p whatsapp -c "Message 1"`
- **Line 420**: `mv Pending_Approval/POST_*_wa_001.md Approved/`
- **Line 433**: `python scripts/trigger_posts.py -p whatsapp -c "Message 2"`
- **Line 434**: `mv Pending_Approval/POST_*_wa_002.md Approved/`
- **Line 446**: `python scripts/trigger_posts.py -p whatsapp -c "Message 3"`
- **Line 447**: `mv Pending_Approval/POST_*_wa_003.md Approved/`
- **Line 459**: `ls -la session/`

### Troubleshooting Section
- **Line 479**: `playwright install chromium firefox`
- **Line 480**: `pkill -f social_media_executor`
- **Line 482**: `python scripts/master_orchestrator.py`
- **Line 487**: `ps aux | grep master_orchestrator`
- **Line 490**: `tail -20 Logs/orchestrator_*.log`
- **Line 496**: `rm -rf session/*`
- **Line 503**: `mkdir -p Pending_Approval Approved Done Logs session`
- **Line 504**: `chmod 755 Pending_Approval Approved Done`

---

## 📧 GMAIL TEST GUIDE (612 lines total)

### Test 1: Basic Gmail Email Creation
- **Line 24-27**: `python scripts/trigger_posts.py -p gmail -c "This is the email body content." -t "Email Subject" --preview`
- **Line 57**: `ls Pending_Approval/ | grep "_gm_"`
- **Line 60**: `cat Pending_Approval/POST_20260329_101534_gm_abc123.md`

### Test 2: Gmail Default Content
- **Line 84**: `python scripts/trigger_posts.py -p gmail --preview`
- **Line 109**: `cat Pending_Approval/POST_*_gm_*.md | grep -A 15 "# Professional"`

### Test 3: Gmail Orchestrator Detection
- **Line 134**: `python scripts/master_orchestrator.py`
- **Line 139**: `python scripts/trigger_posts.py -p gmail -c "Testing orchestrator" -t "Test"`
- **Line 144**: `mv Pending_Approval/POST_*_gm_*.md Approved/`

### Test 4: Gmail Executor Processing
- **Line 184**: `ls Done/ | grep "_gm_"`
- **Line 187**: `ls Approved/ | grep "_gm_" | wc -l`

### Test 5: Gmail Email Subject
- **Line 213-215**: `python scripts/trigger_posts.py -p gmail -c "This is the email body." -t "Important Update from Team" --preview`
- **Line 221**: `cat Pending_Approval/POST_*_gm_*.md | head -20`
- **Line 231**: `mv Pending_Approval/POST_*_gm_*.md Approved/`

### Test 6: Gmail Performance Timing
- **Line 256**: `date "+%H:%M:%S"`
- **Line 257**: `python scripts/trigger_posts.py -p gmail -c "Perf test" -t "Subject"`
- **Line 263**: `date "+%H:%M:%S"`
- **Line 264**: `mv Pending_Approval/POST_*_gm_*.md Approved/`

### Test 7: Gmail Batch Processing
- **Line 296**: `python scripts/trigger_posts.py -p gmail -c "Email 1" -t "Email 1" && sleep 10`
- **Line 298**: `python scripts/trigger_posts.py -p gmail -c "Email 2" -t "Email 2" && sleep 10`
- **Line 300**: `python scripts/trigger_posts.py -p gmail -c "Email 3" -t "Email 3" && sleep 10`
- **Line 302**: `python scripts/trigger_posts.py -p gmail -c "Email 4" -t "Email 4" && sleep 10`
- **Line 304**: `python scripts/trigger_posts.py -p gmail -c "Email 5" -t "Email 5"`
- **Line 307**: `ls Pending_Approval/ | grep "_gm_" | wc -l`
- **Line 309**: `mv Pending_Approval/POST_*_gm_*.md Approved/`
- **Line 311**: `ls Approved/ | grep "_gm_" | wc -l`
- **Line 328**: `ls Done/ | grep "_gm_" | wc -l`
- **Line 331**: `ls Approved/ | grep "_gm_" | wc -l`

### Test 8: Gmail Error Recovery
- **Line 355**: `python scripts/trigger_posts.py -p gmail -c "Error test" -t "Subject"`
- **Line 356**: `mv Pending_Approval/POST_*_gm_*.md Approved/`

### Test 9: Gmail Content Formatting
- **Line 396-399**: `python scripts/trigger_posts.py -p gmail -c "This is a test email with special text: **bold** #hashtag @mention \"quotes\"" -t "Test Subject" --preview`
- **Line 404**: `cat Pending_Approval/POST_*_gm_*.md | grep -A 5 "^#"`
- **Line 411**: `mv Pending_Approval/POST_*_gm_*.md Approved/`

### Test 10: Gmail Session Persistence
- **Line 438**: `python scripts/trigger_posts.py -p gmail -c "Email 1" -t "Subj 1"`
- **Line 439**: `mv Pending_Approval/POST_*_gm_001.md Approved/`
- **Line 452**: `python scripts/trigger_posts.py -p gmail -c "Email 2" -t "Subj 2"`
- **Line 453**: `mv Pending_Approval/POST_*_gm_002.md Approved/`
- **Line 466**: `python scripts/trigger_posts.py -p gmail -c "Email 3" -t "Subj 3"`
- **Line 467**: `mv Pending_Approval/POST_*_gm_003.md Approved/`
- **Line 478**: `ls -la session/`

### Test 11: Gmail Single Recipient
- **Line 501-504**: `python scripts/trigger_posts.py -p gmail -c "Hello, this email is just for you!" -t "Personal Message" --preview`
- **Line 509**: `mv Pending_Approval/POST_*_gm_*.md Approved/`

### Test 12: Gmail Multi-Recipient
- **Line 533-536**: `python scripts/trigger_posts.py -p gmail -c "Hello team, this is for everyone!" -t "Team Update" --preview`
- **Line 541**: `mv Pending_Approval/POST_*_gm_*.md Approved/`

### Troubleshooting Section
- **Line 562**: `playwright install chromium firefox`
- **Line 563**: `pkill -f social_media_executor`
- **Line 565**: `python scripts/master_orchestrator.py`
- **Line 570**: `ps aux | grep master_orchestrator`
- **Line 573**: `tail -20 Logs/orchestrator_*.log`
- **Line 579**: `rm -rf session/*`
- **Line 586**: `mkdir -p Pending_Approval Approved Done Logs session`
- **Line 587**: `chmod 755 Pending_Approval Approved Done`

---

## 🔵 LINKEDIN TEST GUIDE (1200+ lines total)

### Test 1: Basic LinkedIn Post Creation
- **Line 23**: `cd /path/to/project`
- **Line 26**: `pwd`
- **Line 32**: `python scripts/trigger_posts.py -p linkedin -c "Test post from automation system" --preview`
- **Line 64**: `ls Pending_Approval/ | grep "POST_.*_lin_"`
- **Line 73**: `cat Pending_Approval/POST_20260329_101534_lin_abc123.md`

### Test 2: LinkedIn Post with Custom Title
- **Line 102-105**: `python scripts/trigger_posts.py -p linkedin -c "Custom content here" -t "My Custom Title" --preview`
- **Line 137**: `cat Pending_Approval/POST_20260329_101534_lin_custom.md`
- **Line 147**: `grep "^title:" Pending_Approval/POST_20260329_101534_lin_custom.md`
- **Line 151**: `grep "^# My Custom Title" Pending_Approval/POST_20260329_101534_lin_custom.md`

### Test 3: LinkedIn Default Content
- **Line 174**: `python scripts/trigger_posts.py -p linkedin --preview`
- **Line 206**: `cat Pending_Approval/POST_20260329_101600_lin_xyz789.md`

### Test 4: LinkedIn File Format Validation
- **Line 233**: `python scripts/trigger_posts.py -p linkedin -c "Format validation test" -t "Test Title"`
- **Line 239**: `ls Pending_Approval/ | grep "_lin_" | tail -1`
- **Line 243**: `FILENAME=$(ls Pending_Approval/ | grep "_lin_" | tail -1)`
- **Line 244**: `echo $FILENAME`
- **Line 250**: `cat Pending_Approval/$FILENAME`
- **Line 268**: `grep "^platform:" Pending_Approval/$FILENAME`
- **Line 272**: `grep "^title:" Pending_Approval/$FILENAME`
- **Line 276**: `grep "^type:" Pending_Approval/$FILENAME`
- **Line 280**: `grep "^status:" Pending_Approval/$FILENAME`
- **Line 284-291**: `for field in "platform:" "title:" "from:" "type:" "priority:" "status:" "created_at:" "requires_approval:"; do...`

### Test 5: LinkedIn Orchestrator Detection
- **Line 319**: `python scripts/master_orchestrator.py`
- **Line 339**: `python scripts/trigger_posts.py -p linkedin -c "Testing orchestrator detection"`
- **Line 351**: `ls Pending_Approval/ | grep "_lin_"`
- **Line 355**: `mv Pending_Approval/POST_20260329_101534_lin_test1.md Approved/`
- **Line 358**: `ls Approved/ | grep "_lin_"`
- **Line 362**: `ls Pending_Approval/ | grep "_lin_" | wc -l`

### Test 6: LinkedIn Executor Processing
- **Line 410**: `ls Done/ | grep "_lin_"`
- **Line 414**: `ls Approved/ | grep "_lin_" | wc -l`
- **Line 418**: `ls Done/ | grep "processed_POST.*_lin_" | wc -l`
- **Line 425**: `grep "lin_" Logs/orchestrator_*.log | grep -E "Processing|SUCCESS"`

### Test 7: LinkedIn Batch Processing
- **Line 467**: `python scripts/trigger_posts.py -p linkedin -c "Post 1: First update" -t "Post 1" --preview`
- **Line 469**: `sleep 10`
- **Line 472**: `python scripts/trigger_posts.py -p linkedin -c "Post 2: Second update" -t "Post 2" --preview`
- **Line 474**: `sleep 10`
- **Line 477**: `python scripts/trigger_posts.py -p linkedin -c "Post 3: Third update" -t "Post 3" --preview`
- **Line 480**: `ls Pending_Approval/ | grep "_lin_" | wc -l`
- **Line 487**: `mv Pending_Approval/POST_*_lin_*.md Approved/`
- **Line 490**: `ls Approved/ | grep "_lin_" | wc -l`
- **Line 494**: `ls Pending_Approval/ | grep "_lin_" | wc -l`
- **Line 520**: `ls Done/ | grep "processed_POST.*_lin_" | wc -l`
- **Line 524**: `ls Approved/ | grep "_lin_" | wc -l`
- **Line 528-529**: `echo "Processed LinkedIn posts:"`
- **Line 529**: `ls Done/ | grep "processed_POST.*_lin_"`
- **Line 533**: `grep "_lin_" Logs/orchestrator_*.log | grep "SUCCESS" | wc -l`

### Test 8: LinkedIn Error Recovery
- **Line 562**: `python scripts/trigger_posts.py -p linkedin -c "Error recovery test"`
- **Line 568**: `mv Pending_Approval/POST_*_lin_*.md Approved/`

### Test 9: LinkedIn Session Persistence
- **Line 639**: `python scripts/trigger_posts.py -p linkedin -c "Post 1" -t "Session Test 1"`
- **Line 642**: `mv Pending_Approval/POST_*_lin_*.md Approved/`
- **Line 660**: `watch "ls Done/ | grep '_lin_' | wc -l"`
- **Line 668**: `python scripts/trigger_posts.py -p linkedin -c "Post 2" -t "Session Test 2"`
- **Line 671**: `mv Pending_Approval/POST_*_lin_*.md Approved/`
- **Line 688**: `python scripts/trigger_posts.py -p linkedin -c "Post 3" -t "Session Test 3"`
- **Line 691**: `mv Pending_Approval/POST_*_lin_*.md Approved/`
- **Line 708**: `ls -la session/`
- **Line 712**: `ls session/ | wc -l`
- **Line 716**: `grep "session" Logs/orchestrator_*.log | head -10`
- **Line 725**: `grep "_lin_" Logs/orchestrator_*.log | grep "SUCCESS"`

### Test 10: LinkedIn Content Preservation
- **Line 752-756**: `python scripts/trigger_posts.py -p linkedin -c "Testing with 🚀 emoji, @mentions, #hashtags and \"quotes\" and line\nbreaks too!" -t "Special Content Test" --preview`
- **Line 779**: `cat Pending_Approval/POST_*_lin_*.md`
- **Line 785**: `grep "🚀" Pending_Approval/POST_*_lin_*.md`
- **Line 789**: `grep "@mentions" Pending_Approval/POST_*_lin_*.md`
- **Line 793**: `grep "#hashtags" Pending_Approval/POST_*_lin_*.md`
- **Line 797**: `grep '"quotes"' Pending_Approval/POST_*_lin_*.md`
- **Line 801**: `grep -A 2 "Special Content Test" Pending_Approval/POST_*_lin_*.md | grep "breaks"`
- **Line 808**: `mv Pending_Approval/POST_*_lin_*.md Approved/`

### Test 11: LinkedIn Performance Timing
- **Line 856**: `date "+%H:%M:%S"`
- **Line 860**: `python scripts/trigger_posts.py -p linkedin -c "Performance test" -t "Perf Test"`
- **Line 868**: `date "+%H:%M:%S"`
- **Line 872**: `mv Pending_Approval/POST_*_lin_*.md Approved/`
- **Line 902**: `grep "_lin_" Logs/orchestrator_*.log | grep "Processing\|Executing\|SUCCESS"`
- **Line 919-939**: `for i in {1..5}; do ... python scripts/trigger_posts.py -p linkedin -c "Perf Test $i" ... done`

### Test 12: LinkedIn HITL Workflow
- **Line 986-988**: `python scripts/trigger_posts.py -p linkedin -c "Important announcement for our LinkedIn audience" -t "Company Update"`
- **Line 1000**: `cat Pending_Approval/POST_*_lin_*.md`
- **Line 1022**: `mv Pending_Approval/POST_*_lin_*.md Approved/`
- **Line 1025**: `ls Approved/ | grep "_lin_"`
- **Line 1029**: `ls Pending_Approval/ | grep "_lin_" | wc -l`
- **Line 1050**: `ls Done/ | grep "_lin_"`
- **Line 1054**: `ls Approved/ | grep "_lin_" | wc -l`
- **Line 1058**: `grep "_lin_.*Company Update" Logs/orchestrator_*.log`

### Test 13: LinkedIn Multi-Platform Batch Testing
- **Line 1113**: `python scripts/master_orchestrator.py`
- **Line 1124**: `python scripts/run_workflow_test.py --batch`
- **Line 1179**: `ls Done/ | grep "processed_POST" | wc -l`
- **Line 1183**: `ls Done/ | grep "processed_POST.*_lin_"`
- **Line 1187**: `ls Approved/ | grep "POST" | wc -l`
- **Line 1191**: `ls Logs/error_*.png 2>/dev/null | wc -l`
- **Line 1199**: `echo "Platform Processing Summary:"`

---

## 📊 SUMMARY STATISTICS

### Total Terminal Commands by Platform

| Platform | Test Guide | Total Commands | Line Range |
|----------|-----------|-----------------|-----------|
| Facebook | facebook_test_guide.md | 45+ commands | Lines 28-778 |
| Twitter | twitter_test_guide.md | 38+ commands | Lines 23-552 |
| Instagram | instagram_test_guide.md | 32+ commands | Lines 22-487 |
| WhatsApp | whatsapp_test_guide.md | 32+ commands | Lines 22-504 |
| Gmail | gmail_test_guide.md | 36+ commands | Lines 24-587 |
| LinkedIn | linkedin_test_guide.md | 52+ commands | Lines 23-1199 |

### **TOTAL ACROSS ALL 6 GUIDES: 235+ TERMINAL COMMANDS**

---

## 🎯 QUICK REFERENCE

### Most Common Commands (Used in Multiple Tests)

**File Creation:**
- `python scripts/trigger_posts.py -p [platform] -c "[content]" --preview`
- `python scripts/trigger_posts.py -p [platform] -c "[content]" -t "[title]"`

**File Operations:**
- `ls Pending_Approval/ | grep "_[code]_"`
- `cat Pending_Approval/POST_*`
- `mv Pending_Approval/POST_*_[code]_*.md Approved/`
- `ls Done/ | grep "_[code]_"`
- `ls Approved/ | grep "_[code]_" | wc -l`

**Timing & Monitoring:**
- `date "+%H:%M:%S"`
- `watch "ls Done/ | grep '_[code]_' | wc -l"`
- `grep "_[code]_" Logs/orchestrator_*.log | grep "SUCCESS"`

**Session & Troubleshooting:**
- `ls -la session/`
- `python scripts/master_orchestrator.py`
- `ps aux | grep master_orchestrator`
- `tail -20 Logs/orchestrator_*.log`

---

## ✅ VERIFICATION CHECKLIST

All 6 test guides include terminal commands at:
- ✅ Step-by-step instructions for each test
- ✅ Actual, copy-paste ready commands
- ✅ Expected output examples
- ✅ Verification commands with results
- ✅ Troubleshooting section with commands
- ✅ Batch processing with multiple commands

---

**Status:** ✅ COMPLETE - All 235+ terminal commands mapped with exact line numbers
**Date:** 2026-03-30
**Version:** 2.0
