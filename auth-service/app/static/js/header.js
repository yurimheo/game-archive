document.addEventListener("DOMContentLoaded", function () {
    // Login 버튼 클릭 시 URL 이동
    const loginButton = document.getElementById('loginButton');
    if (loginButton) {
        loginButton.addEventListener('click', function () {
            const url = this.getAttribute('data-url'); // 버튼의 data-url 속성 값 가져오기
            if (url) window.location.href = url; // URL로 이동
        });
    }

    // Sign Up 버튼 클릭 시 URL 이동
    const signupButton = document.getElementById('signupButton');
    if (signupButton) {
        signupButton.addEventListener('click', function () {
            const url = this.getAttribute('data-url'); // 버튼의 data-url 속성 값 가져오기
            if (url) window.location.href = url; // URL로 이동
        });
    }

    // My Page 버튼 클릭 시 URL 이동
    const mypageButton = document.getElementById('mypageButton');
    if (mypageButton) {
        mypageButton.addEventListener('click', function () {
            const url = this.getAttribute('data-url'); // 버튼의 data-url 속성 값 가져오기
            if (url) window.location.href = url; // URL로 이동
        });
    }

    // Logout 버튼 클릭 시 동작 처리
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function (event) {
            event.preventDefault(); // 기본 폼 동작 방지
            const form = this.closest('form'); // 버튼이 포함된 폼 가져오기
            if (form) form.submit(); // 폼 제출 (로그아웃 처리)
        });
    }

    // 서브텍스트 애니메이션
    const subtitleText = "AM 11, Every Day"; // 애니메이션에 사용할 텍스트
    const subtitleElement = document.getElementById('subtitle'); // 텍스트가 표시될 요소
    if (subtitleElement) {
        subtitleText.split('').forEach((char, index) => {
            const span = document.createElement('span'); // 개별 문자를 span으로 생성
            span.innerHTML = char === ' ' ? '&nbsp;' : char; // 공백은 &nbsp;로 처리
            span.className = 'letter'; // 애니메이션 효과를 위한 클래스 추가
            span.style.animationDelay = `${index * 0.1}s`; // 각 문자에 지연시간 적용
            subtitleElement.appendChild(span); // 요소에 추가
        });
    }

    // 메인 텍스트 타이핑 효과
    const mainText = "Limited Time Deal"; // 타이핑 효과에 사용할 텍스트
    const typewriterElement = document.getElementById('typewriter'); // 텍스트가 표시될 요소
    if (typewriterElement) {
        let i = 0; // 현재 문자 인덱스
        const speed = 100; // 타이핑 속도 (밀리초)

        function typeWriter() {
            if (i < mainText.length) {
                typewriterElement.textContent += mainText.charAt(i); // 한 글자씩 추가
                i++;
                setTimeout(typeWriter, speed); // 다음 글자를 타이핑
            }
        }

        typeWriter(); // 타이핑 시작
    }

    // 드롭다운 버튼 토글
    document.querySelectorAll('.hyl-dropdown-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.stopPropagation(); // 클릭 이벤트 전파 방지
            const dropdown = this.parentElement; // 부모 요소 가져오기
            dropdown.classList.toggle('show'); // 드롭다운 메뉴 표시/숨기기
        });
    });

    // 햄버거 메뉴 토글
    const hamburgerMenuToggle = document.getElementById('hamburger-menuToggle'); // 햄버거 메뉴 버튼
    const hamburgerDropdownMenu = document.getElementById('hamburger-dropdownMenu'); // 드롭다운 메뉴

    if (hamburgerMenuToggle && hamburgerDropdownMenu) {
        hamburgerMenuToggle.addEventListener('click', () => {
            hamburgerDropdownMenu.classList.toggle('hidden'); // 드롭다운 메뉴 표시/숨기기
        });
    }
});
