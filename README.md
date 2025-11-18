# مشروع التحكم عن بعد التعليمي (Remote Administration Tool - Educational)

**تنبيه مهم | Important Notice**  
هذا المشروع تم إنشاؤه لأغراض تعليمية فقط.  
**لا تستخدم هذا البرنامج لأي نشاط غير قانوني أو ضار.**  
This project is created **for educational purposes only**.  
**Do not use this software for any illegal or malicious activities.**

---

## وصف المشروع | Project Description
هذا المشروع عبارة عن أداة للتحكم عن بعد (RAT) تستخدم لغة Python، تمكنك من تنفيذ أوامر على جهاز بعيد، مثل:  
- تغيير الخلفية  
- التقاط لقطات شاشة  
- إدارة الملفات  
- تحميل ورفع الملفات  
- التحكم بعمليات النظام  
- تشغيل وإيقاف الجهاز  

This project is a **Remote Administration Tool (RAT)** built in Python.  
It allows you to execute commands on a remote machine, such as:  
- Change wallpaper  
- Take screenshots  
- Manage files  
- Upload and download files  
- Monitor system processes  
- Shutdown or restart the system  

---

## المكونات | Components
- **Client (victim.py)**: البرنامج الذي يُشغَّل على الجهاز المستهدف.  
- **Server (server.py)**: البرنامج الذي يُشغَّل على جهازك للتحكم بالـ Client.  

---

## المتطلبات | Requirements
- Python 3.x  
- مكتبات Python:
  - `PIL` أو `Pillow`
  - `psutil`
  - `tqdm`

---

## طريقة التشغيل | How to Run
1. شغّل `server.py` على جهازك واستمع للاتصالات.  
2. شغّل `victim.py` على الجهاز التجريبي الذي تريد التحكم فيه.  
3. استخدم أوامر مثل:  
   - `exit` لإنهاء الاتصال  
   - `cd <path>` لتغيير المجلد  
   - `download <file>` لتحميل ملف  
   - `upload <file>` لرفع ملف  
   - `screenshot` لأخذ صورة للشاشة  
   - `bg <image_path>` لتغيير الخلفية  
   - `action_list` لعرض العمليات الجارية  
   - `shutdown <seconds>` لإيقاف تشغيل الجهاز  
   - `restart <seconds>` لإعادة تشغيل الجهاز  
   - `shutdown_abort` لإلغاء عملية الإيقاف  

1. Run `server.py` on your machine to listen for connections.  
2. Run `victim.py` on the target (test) machine.  
3. Use commands such as:  
   - `exit` to terminate the connection  
   - `cd <path>` to change directory  
   - `download <file>` to download a file  
   - `upload <file>` to upload a file  
   - `screenshot` to capture the screen  
   - `bg <image_path>` to change wallpaper  
   - `action_list` to list running processes  
   - `shutdown <seconds>` to shutdown the system  
   - `restart <seconds>` to restart the system  
   - `shutdown_abort` to abort shutdown  

---

## ملاحظات أمنية | Security Notes
- هذا المشروع لغرض التعليم فقط ولا يُنصح باستخدامه خارج بيئة اختبارية.  
- تجنب تشغيله على أجهزة أشخاص آخرين بدون إذنهم.  
- يمكن استخدامه لفهم الشبكات، البروتوكولات، وأمان البرمجيات.

This project is **for educational purposes only** and should **only be used in a controlled environment**.  
Do not run it on devices you do not own or have explicit permission to access.  
Use it to learn about networking, protocols, and software security.

---

## الترخيص | License
غير مخصص للاستخدام التجاري أو الضار. مفتوح للدراسة والتعلم فقط.  
Not intended for commercial or malicious use. Open for educational study only.
