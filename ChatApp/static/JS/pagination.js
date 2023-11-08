// if (uid === 教師IDアカウント) を修正予定

const deleteChannelModal = document.getElementById("delete-channel-modal");

//STEPは6ではなく5に変更。
const pagination = async () => {
  let page = 1;
  const STEP = 6;

  const TOTAL =
    channels.length % STEP == 0
      ? channels.length / STEP
      : Math.floor(channels.length / STEP) + 1;

  const paginationUl = document.querySelector(".pagination");
  let pageCount = 0;
  while (pageCount < TOTAL) {
    let pageNumber = document.createElement("li");
    pageNumber.dataset.pageNum = pageCount + 1;
    pageNumber.innerText = pageCount + 1;
    paginationUl.appendChild(pageNumber);

    pageNumber.addEventListener("click", (e) => {
      const targetPageNum = e.target.dataset.pageNum;
      page = Number(targetPageNum);
      show(page, STEP);
      colorPaginationNum();
    });
    pageCount++;
  }
  const show = (page, STEP) => {
    const ul = document.querySelector(".channel-box");
    ul.innerHTML = "";
    const firstChannelInPage = (page - 1) * STEP + 1;
    const lastChannelInPage = page * STEP;

    channels.forEach((channel, i) => {
      if (i < firstChannelInPage - 1 || i > lastChannelInPage - 1) return;
      const a = document.createElement("a");
      const li = document.createElement("li");
      const channelURL = `/detail/${channel.id}`;
      a.innerText = channel.name;
      a.setAttribute("href", channelURL);
      li.appendChild(a);

      //削除ボタンのアイコン変更
      if (uid === channel.uid) {
        const deleteButton = document.createElement("button");
        deleteButton.innerHTML =
          '<i class="fa-regular fa-trash-can fa-lg"></i>';
        deleteButton.classList.add("delete-button");
        li.appendChild(deleteButton);

        deleteButton.addEventListener("click", () => {
          deleteChannelModal.style.display = "flex";
          const confirmationButtonLink = document.getElementById(
            "delete-confirmation-link"
          );

          const channelURL = `/delete/${channel.id}`;
          confirmationButtonLink.setAttribute("href", channelURL);
        });
      }
    });
      //もし自分のユーザーIDが先生用ユーザーIDの場合チャンネル追加ボタンを追加
    if (uid === 教師IDアカウント) {
      const addChannelButton = document.createElement("button");
      addChannelButton.innerHTML =
        '<i class="fa-solid fa-circle-plus fa-lg"></i>';
      addChannelButton.classList.add("add-channel-button");
      addChannelPagination.appendChild(addChannelButton);
    };
  };
  const colorPaginationNum = () => {

    const paginationArr = [...document.querySelectorAll(".pagination li")];
    paginationArr.forEach((page) => {
      page.classList.remove("colored");
    });
    // 選択されているページにclass = "colored"を追加（文字色が変わる）
    paginationArr[page - 1].classList.add("colored");
  };

  show(page, STEP);
  colorPaginationNum();

  document.getElementById("prev").addEventListener("click", () => {
    if (page <= 1) return;
    page = page - 1;
    show(page, STEP);
    colorPaginationNum();
    loadAddChannelButton();
  });

  document.getElementById("next").addEventListener("click", () => {
    if (page >= channels.length / STEP) return;
    page = page + 1;
    show(page, STEP);
    colorPaginationNum();
    loadAddChannelButton();
  });
};

window.onload = () => {

  pagination().then(loadAddChannelButton);
};
