const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const result = document.getElementById("result");

uploadBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    result.innerText = "請先選擇圖片";
    return;
  }
  const file = fileInput.files[0];
  const form = new FormData();
  form.append("image", file);

  result.innerText = "上傳中…";

  try {
    const resp = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: form
    });
    const data = await resp.json();
    if (data.ok) {
      result.innerHTML = `上傳成功：${data.filename}`;
    } else {
      result.innerText = "錯誤：" + (data.error || "未知錯誤");
    }
  } catch (e) {
    result.innerText = "無法連線到後端，請確認 Flask 伺服器是否正在執行。";
    console.error(e);
  }
});
