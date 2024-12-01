document.getElementById('loginButton').addEventListener('click', function () {
    const url = this.getAttribute('data-url'); // 버튼의 data-url 속성 값 가져오기
    window.location.href = url; // URL로 이동
});

document.getElementById('signupButton').addEventListener('click', function () {
    const url = this.getAttribute('data-url'); // 버튼의 data-url 속성 값 가져오기
    window.location.href = url; // URL로 이동
});

// 서브텍스트 애니메이션
const subtitleText = "AM 11, Every Day";
const subtitleElement = document.getElementById('subtitle');

subtitleText.split('').forEach((char, index) => {
    const span = document.createElement('span');
    // 공백 문자는 &nbsp;로 처리하여 띄어쓰기 적용
    span.innerHTML = char === ' ' ? '&nbsp;' : char;
    span.className = 'letter';
    span.style.animationDelay = `${index * 0.1}s`;
    subtitleElement.appendChild(span);
});

// 메인 타이핑 효과
const mainText = "Limited Time Deal";
const speed = 100;
let i = 0;
const typewriterElement = document.getElementById('typewriter');

function typeWriter() {
    if (i < mainText.length) {
        typewriterElement.textContent += mainText.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}

typeWriter();

document.querySelectorAll('.hyl-dropdown-button').forEach(button => {
button.addEventListener('click', function (event) {
    event.stopPropagation();
    const dropdown = this.parentElement;
    dropdown.classList.toggle('show');
});
});

// 햄버거 메뉴 토글
const hamburgerMenuToggle = document.getElementById('hamburger-menuToggle');
const hamburgerDropdownMenu = document.getElementById('hamburger-dropdownMenu');

if (hamburgerMenuToggle && hamburgerDropdownMenu) {
    hamburgerMenuToggle.addEventListener('click', () => {
        hamburgerDropdownMenu.classList.toggle('hidden'); 
    });
}