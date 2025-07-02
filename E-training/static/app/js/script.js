document.addEventListener('DOMContentLoaded', function() {
    const videoPlayer = document.getElementById('videoPlayer');
    const lectureList = document.getElementById('lectureList');
    const lectureStatus = document.getElementById('lectureStatus');
    
    // Handle lecture selection
    lectureList.addEventListener('click', function(e) {
        const lectureItem = e.target.closest('.lecture-item');
        
        if (!lectureItem || lectureItem.classList.contains('locked')) {
            return;
        }

        // Update active state
        document.querySelectorAll('.lecture-item').forEach(item => {
            item.classList.remove('active');
        });
        lectureItem.classList.add('active');

        // Update video
        const videoId = lectureItem.dataset.videoId;
        const videoTitle = lectureItem.dataset.title;
        
        videoPlayer.src = `https://www.youtube.com/embed/${videoId}`;
        videoPlayer.title = videoTitle;

        // Update status badge
        const isPreview = lectureItem.querySelector('.lecture-badge')?.textContent === 'Preview';
        lectureStatus.textContent = isPreview ? 'Free Preview' : 'Full Lecture';
    });

    // Initialize first lecture as active
    const firstLecture = lectureList.querySelector('.lecture-item');
    if (firstLecture) {
        firstLecture.classList.add('active');
    }

    // Handle enrollment form submission
    const enrollForm = document.querySelector('form');
    const enrollButton = document.querySelector('.enroll-button');

    if (enrollForm && enrollButton) {
        enrollForm.addEventListener('submit', function() {
            enrollButton.disabled = true;
            enrollButton.innerHTML = `
                <i class="fas fa-spinner fa-spin"></i>
                Enrolling...
            `;
        });
    }
});