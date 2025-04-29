const form = document.querySelector("form");
const result_box = document.querySelector(".result_wrapper");
const result_outputs = document.querySelectorAll(".output");
const versions = document.querySelector(".versions");
const allVersions = document.querySelectorAll(".version");
const allLabels = document.querySelectorAll(".form__label");
let hiddenFormGroup = document.querySelector(".form__group");
let selectedVersion = "Intubed";

const postData = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Failed to fetch:", error);
    }
};

const selectVersion = (e) => {
    e.preventDefault();
    if (e.target.tagName !== "A") return;

    selectedVersion = e.target.innerText;

    allVersions.forEach(v => v.classList.remove("btn--dark"));
    e.target.classList.add("btn--dark");

    allLabels.forEach((label) => {
        if (label.innerText === selectedVersion) {
            hiddenFormGroup.classList.remove("hide");
            hiddenFormGroup.querySelector("select").selectedIndex = 0;
            label.parentElement.classList.add("hide");
            label.parentElement.querySelector("select").value = null;
            hiddenFormGroup = label.parentElement;
        } else if (["ICU", "Intubed"].includes(selectedVersion)) {
            hiddenFormGroup.classList.remove("hide");
            hiddenFormGroup.querySelector("select").selectedIndex = 0;
        }
    });
};

versions.addEventListener("click", selectVersion);


const getPrediction = async () => {
    document.querySelector(".model-version").value = selectedVersion; // Set model-version hidden input

    const formData = new FormData(form);
    let data = { 'model': selectedVersion };

    formData.forEach((value, key) => {
        data[key] = value;
    });

    const response = await postData("/predict", data);
    if (response) {
        updateUI(response);
    }

}

//getPrediction();

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await getPrediction();

});


const updateUI = (data) => {
    result_outputs[0].innerText = data["Model"];
    result_outputs[1].innerText = data["Prediction"];
    result_outputs[2].innerText = data["Probability"];

    document.querySelector(".probability-fill").style.width = data["Probability"]

    result_box.classList.remove("hide");
};

document.querySelector(".close").addEventListener("click", () => {
    result_box.classList.add("hide");
});
