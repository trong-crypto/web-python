document.addEventListener('DOMContentLoaded', function() {
    // Tự động đóng thông báo sau 5 giây
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Xác nhận trước khi xóa hoặc thay đổi trạng thái
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
    
    // Hiển thị thời gian hiện tại trong form đặt thiết bị
    const startTimeInput = document.querySelector('input[name="start_time"]');
    const endTimeInput = document.querySelector('input[name="end_time"]');
    
    if (startTimeInput && endTimeInput) {
        const now = new Date();
        const later = new Date(now.getTime() + 2 * 60 * 60 * 1000); // 2 giờ sau
        
        // Định dạng cho datetime-local input
        const formatDate = (date) => {
            return date.toISOString().slice(0, 16);
        };
        
        if (!startTimeInput.value) {
            startTimeInput.value = formatDate(now);
        }
        if (!endTimeInput.value) {
            endTimeInput.value = formatDate(later);
        }
    }
});