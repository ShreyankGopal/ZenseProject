const url = window.location.href;

    $.ajax({
        type: 'GET',
        url: `${url}`,
        success: function(response) {
            const questionList = response.data;
            const questionDiv = document.getElementById('question-list');

            questionList.forEach(questionObj => {
                const question = Object.keys(questionObj)[0];
                const answers = questionObj[question];

                const questionElem = document.createElement('div');
                questionElem.innerHTML = `<p>${question}</p>`;

                answers.forEach(answer => {
                    const radioInput = `<input type="radio" name="${question}" value="${answer}" /> ${answer}<br>`;
                    questionElem.innerHTML += `${radioInput}`;
                });

                questionDiv.appendChild(questionElem);
            });
        },
        error: function(error) {
            console.error(error);
        }
    });