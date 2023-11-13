// チャンネルを登録する時の処理
const addChannelModal = document.getElementById("add-channel-modal");
const addPageButtonClose = document.getElementById("add-page-close-button");
const addChannelConfirmButton = document.getElementById("add-channel-confirmation-button");
const addChannelButton = document.getElementById("add-channel-button");

// モーダル表示ボタンが押された時にモーダルを表示する
addChannelButton.addEventListener("click", () => {
  addChannelModal.style.display = "flex";
});

// モーダル内のXボタンが押された時にモーダルを非表示にする
addPageButtonClose.addEventListener("click", () => {
  addChannelModal.style.display = "none";
});

// 画面のどこかが押された時にモーダルを非表示にする
addEventListener("click", (e) => {
  if (e.target == addChannelModal) {
    addChannelModal.style.display = "none";
  }
});
