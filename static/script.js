document.addEventListener("DOMContentLoaded", function () {

    const fileInput =
        document.querySelector('input[type="file"]');

    if (fileInput) {

        fileInput.addEventListener(
            "change",
            function () {

                if (this.files.length > 0) {

                    console.log(
                        "Resume selected:",
                        this.files[0].name
                    );

                }

            }
        );

    }

});