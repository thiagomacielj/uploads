const form = document.getElementById('uploadForm');
const progressBar = document.getElementById('progressBar');
const toast = document.getElementById('toast');

form.addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(form);
    const xhr = new XMLHttpRequest();

    xhr.open('POST', '/upload', true);

    xhr.upload.addEventListener('progress', function (e) {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = percent + '%';
            progressBar.textContent = percent + '%';
        }
    });

    xhr.onload = function () {
        if (xhr.status === 200) {
            // Mostra toast
            toast.classList.remove('hidden');
            setTimeout(() => {
                toast.classList.add('hidden');
                window.location.href = '/visualizar'; // redireciona após upload
            }, 2000);
        } else {
            alert('Erro no upload');
        }
    };

    xhr.send(formData);
});
