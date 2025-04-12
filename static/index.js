const versions = document.querySelector(".versions")
const allVersions = document.querySelectorAll(".version")
const allLabels = document.querySelectorAll(".form__label")
let hiddenFormGroup = document.querySelector(".form__group.hide");
hiddenFormGroup.querySelector("select").value = null;

const selectVersion = (e) => {

    e.preventDefault();
    if (e.target.tagName != "A") {
        return;
    }
    const selectedVersion = e.target.innerText;

    // Change Version Button Style (dark theme)
    allVersions.forEach(v => {
        v.classList.remove("btn--dark");
    })
    e.target.classList.add("btn--dark");


    // Remove Selected Target From Form
    allLabels.forEach((label) => {

        if (label.innerText === selectedVersion) {

            // Show Recent Hidden Target
            hiddenFormGroup.classList.remove("hide");
            hiddenFormGroup.querySelector("select").selectedIndex  = 0

            // Hide Selected Target
            label.parentElement.classList.add("hide");
            label.parentElement.querySelector("select").value = null;
            hiddenFormGroup = label.parentElement;
        }

    })


}
versions.addEventListener("click", selectVersion)