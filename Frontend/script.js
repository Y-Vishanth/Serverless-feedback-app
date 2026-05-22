async function submitFeedback() {

    const name =
        document.getElementById("name").value;

    const message =
        document.getElementById("message").value;

    const feedbackData = {
        name: name,
        message: message
    };

    try {

        const response = await fetch(
            "https://dmw4qvvrcl.execute-api.us-east-1.amazonaws.com/dev/submit",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(feedbackData)
            }
        );

        const data = await response.json();

        document.getElementById("response").innerText =
            data.message;

    } catch (error) {

        console.log(error);

        document.getElementById("response").innerText =
            "Error submitting feedback";
    }
}