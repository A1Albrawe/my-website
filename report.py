    <script>
        // توليد رقم معرّف عشوائي فريد لكل زائر لمنع تداخل الرسائل والردود بين المستخدمين
        const uniqueSessionId = "user_" + Math.floor(Math.random() * 900000 + 100000);

        function autoFillUser() {
            let savedUser = localStorage.getItem('snake_last_user');
            if (savedUser) { document.getElementById('userName').value = savedUser; }
        }

        // إرسال الشكوى أو رسالة المحادثة الحية مباشرة لخادم البوت عبر تقنية FETCH
        function handleFormSubmit(event) {
            event.preventDefault();
            
            const user = document.getElementById('userName').value.trim();
            const type = document.getElementById('issueType').value;
            const details = document.getElementById('issueDetails').value.trim();
            
            if (!user || !details) return;

            // إظهار الرسالة في صندوق الشات الخاص بالزائر فوراً للمعاينة
            appendLogItem(type, details, "user-msg");
            document.getElementById('issueDetails').value = "";

            // إرسال البيانات فوراً إلى الخلفية البرمجية لتوصيلها لتليجرام المطور
            fetch('/api/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user: user,
                    type: type,
                    details: details,
                    session_id: uniqueSessionId
                })
            });
        }

        function appendLogItem(type, text, className) {
            const container = document.getElementById('logContainer');
            if(container.innerHTML.includes("لا توجد تقارير")) container.innerHTML = "";
            
            const item = document.createElement('div');
            item.className = "log-item " + className;
            item.innerHTML = `<span style="font-weight:bold;">[${type}]:</span> <span>${text}</span>`;
            container.appendChild(item);
            container.scrollTop = container.scrollHeight;
        }

        // الاستماع لردود المطور القادمة من التليجرام كل ثانيتين بانتظام وعرضها للزائر فوراً
        setInterval(() => {
            fetch('/api/get_reply/' + uniqueSessionId)
            .then(res => res.json())
            .then(data => {
                if (data.status === "found") {
                    appendLogItem("رد المطور 🛠️", data.reply, "admin-reply");
                }
            });
        }, 2000);

        autoFillUser();
    </script>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_TEMPLATE)
