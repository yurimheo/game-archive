document.addEventListener("DOMContentLoaded", function () {
    const apiUrl = "/hyl/api/qna";

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const popularList = document.getElementById("popular-questions");
            const questionsTable = document.getElementById("questions-table");

            // 인기 질문 (조회수 기준 상위 3개)
            const popularQuestions = [...data].sort((a, b) => b.views - a.views).slice(0, 3);
            popularQuestions.forEach((question) => {
                const li = document.createElement("li");
                li.className = "list-group-item";
                li.innerHTML = `<a href="#">${question.title}</a> - 조회수 ${question.views}`;
                popularList.appendChild(li);
            });

            // 전체 질문 목록
            data.forEach((question, index) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <th scope="row">${index + 1}</th>
                    <td><a href="#">${question.title}</a></td>
                    <td>${question.author}</td>
                    <td>${question.views}</td>
                `;
                questionsTable.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching questions:", error));
});

// 질문 등록 페이지로 이동하기
document.addEventListener("DOMContentLoaded", function () {
    const qnaButton = document.querySelector(".qna-button");

    if (qnaButton) {
        qnaButton.addEventListener("click", function () {
            const url = qnaButton.getAttribute("data-url");
            if (url) {
                location.href = url;
            }
        });
    }
});

// 질문 목록 페이지로 이동하기
document.addEventListener("DOMContentLoaded", function () {
    const switchButtons = document.querySelectorAll(".qna-c-switch-button");

    switchButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // 모든 버튼에서 active 클래스 제거
            switchButtons.forEach((btn) => btn.classList.remove("active"));

            // 클릭된 버튼에 active 클래스 추가
            button.classList.add("active");

            // URL 이동 처리
            const url = button.getAttribute("data-url");
            if (url && button.type === "button") {
                location.href = url;
            }
        });
    });
});