const deleteChannelModal = document.getElementById("delete-channel-modal");
const pagination = async () => {
  let page = 1; 
  const STEP = 5; 
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
      a.innerText = channel.channel_name;
      a.setAttribute("href", channelURL);
      li.appendChild(a);

      if (uid === channel.user_id) {
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
      ul.appendChild(li);
    });
  };

  const colorPaginationNum = () => {
    const paginationArr = [...document.querySelectorAll(".pagination li")];
    paginationArr.forEach((page) => {
      page.classList.remove("colored");
    });
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
  pagination();
};
