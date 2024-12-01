
let currentIndex = 0; // 현재 슬라이드 인덱스
    const slides = document.querySelectorAll('.slide');

    function showSlide(index) {
        // 모든 슬라이드 숨김
        slides.forEach((slide) => slide.classList.remove('active'));
        // 현재 슬라이드만 표시
        slides[index].classList.add('active');
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length; // 다음 슬라이드
        showSlide(currentIndex);
    }

    // 5초마다 슬라이드 전환
    setInterval(nextSlide, 5000);

    // 초기 슬라이드 표시
    showSlide(currentIndex);