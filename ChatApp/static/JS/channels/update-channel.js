// チャンネルを更新する時の処理
const updateButton = document.getElementById("channel-update-button");
//channel-update-buttonはとっちさんに合わせる(index.html)
const updateChannelModal = document.getElementById("update-channel-modal");
const updatePageButtonClose = document.getElementById
  ("update-page-close-button");

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateChannelModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateChannelModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateChannelModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateChannelModal) {
      updateChannelModal.style.display = "none";
    }
  });
}