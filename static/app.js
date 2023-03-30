const button = document.querySelector("#show-answers");
const answerDiv = document.querySelector("#answers");
button.addEventListener("click", async (e) => {
  const result = await axios.get("/answers");
  const answers = result.data;
  answerDiv.innerText = JSON.stringify(answers);
});
