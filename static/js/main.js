$(document).ready(function () {

    // ✅ 初始化 DataTable（只初始化一次）
    if (! $.fn.DataTable.isDataTable("#resultTable")) {
        $("#resultTable").DataTable({
            pageLength: 10,
            lengthChange: false,
            info: false
        });
    }

    // 點擊「詳情」按鈕
    $(document).on("click", ".detail-btn", function () {
        const name = $(this).attr("data-name"); // 從 data-name 取得姓名

        fetch("/get_resume_detail", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: name })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // 顯示在 Modal
                document.getElementById("modal-text").textContent = data.text;
                new bootstrap.Modal(document.getElementById("detailModal")).show();
            } else {
                alert("查無資料");
            }
        })
        .catch(err => {
            console.error("AJAX 發生錯誤:", err);
            alert("發生錯誤，請檢查後端 API");
        });
    });

});