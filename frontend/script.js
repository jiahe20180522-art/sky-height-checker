const RENDER_URL = "https://sky-height-checker-2.onrender.com"; // ←換成你的 Render URL

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
    const resp = await fetch(RENDER_URL, {
      method: "POST",
      body: form
    });
    const data = await resp.json();

    if (data.ok) {
      result.innerHTML = `上傳成功<br>身高編號：${data.height}<br>Cloudinary 圖片：<a href="${data.url}" target="_blank">點我查看</a>`;
    } else {
      result.innerText = "錯誤：" + (data.error || "未知錯誤");
    }
  } catch (e) {
    result.innerText = "無法連線到後端，請確認網站是否已部署。";
    console.error(e);
  }
});
