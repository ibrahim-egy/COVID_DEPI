const versions = document.querySelector(".versions")
const allVersions = document.querySelectorAll(".version")
const allLabels = document.querySelectorAll(".form__label")
let hiddenFormGroup = document.querySelector(".form__group");
let selectedVersion = "Intubed"
const selectVersion = (e) => {

    e.preventDefault();
    if (e.target.tagName != "A") {
        return;
    }
    selectedVersion = e.target.innerText;

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
        } else if (["ICU", "Intubed"].includes(selectedVersion)) {
            hiddenFormGroup.classList.remove("hide");
            hiddenFormGroup.querySelector("select").selectedIndex  = 0
        }

    })


}
versions.addEventListener("click", selectVersion)
document.querySelector("form").addEventListener("submit", () => {

    document.querySelector(".model-version").value = selectedVersion;
})

//let data = {}
//
//document.querySelector("form").addEventListener("submit", async (e) => {
//    e.preventDefault();
//
//    const form = e.target;
//    const formData = new FormData(form)
//    data = {
//        'model': selectVersion
//    }
//
//    formData.forEach((value, key) => {
//        data[key] = value;
//    })
//
//    const response = await postData("/predict", data)
//    console.log(response)
//})
//
//const postData = async (url, data) => {
//
//    const response = await fetch(url, {
//      method: "POST",
//      headers: {'Content-Type': 'application/json'},
//      body: JSON.stringify(data)
//    })
//     if (response.ok) {
//
//        const result = response.json()
//        return result;
//     }
//
//}