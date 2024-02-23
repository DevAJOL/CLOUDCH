// Wrap your code in a DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", () => {
  // Your code here
  getVisitCount();
});

const localApi = "http://localhost:7071/api/GetVisitorCounter";
const prodApi = "https://getvisitorcounteer.azurewebsites.net/api/GetVisitorCounter";

const getVisitCount = () => {
  let count = 0;
  console.log("Before fetch"); // Debug message
  fetch(prodApi)
    .then((response) => {
      console.log("After fetch"); // Debug message
      return response.json(); // Parse response as json
    })
    .then((response) => {
      console.log("Website called function API."); // Debug message
      count = response.Count;

      // Get the last two digits of the count
      const lastTwoDigits = count % 100;

      // Get the last digit of the count
      const lastDigit = count % 10;

      // Determine the appropriate suffix based on the last two digits
      let suffix;
      if (
        lastTwoDigits === 11 ||
        lastTwoDigits === 12 ||
        lastTwoDigits === 13
      ) {
        suffix = "th";
      } else {
        const lastDigit = count % 10;
        switch (lastDigit) {
          case 1:
            suffix = "st";
            break;
          case 2:
            suffix = "nd";
            break;
          case 3:
            suffix = "rd";
            break;
          default:
            suffix = "th";
        }
      }

      document.getElementById("counter").innerText = `${count}${suffix}`;
    })
    .catch(function (error) {
      console.error("Error:", error); // Debug message
      console.log(error);
    });
  console.log("Returning count:", count); // Debug message
  return count;
};
