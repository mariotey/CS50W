document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', sent_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
});

//////////////////////////////////////////////////////////////////////////////////////////////////

function load_mailbox(mailbox) {// parameters: inbox, sent, archive

  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#message-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(`GET /emails/${mailbox}`);
    console.log(emails);

    emails.forEach(email => {
      const email_elem = document.createElement("div");
      email_elem.style.cssText =`
        display: flex;  
        border: solid black 2px;
        justify-content: space-between;
      `;

      if (email.read) {
        email_elem.style.cssText = email_elem.style.cssText + "background-color: lightgray;"
      }

      if (mailbox === "inbox") {
        email_elem.innerHTML = `
          <div style="display: flex">
            <div style="width:250px; margin: 5px;">
              <strong>${email.sender}</strong>
            </div>
            <div style="width:250px; margin: 5px;">${email.subject}</div>
          </div>
          <div style="margin: 5px;">${email.timestamp}</div>
        `;
      };

      if (mailbox === "sent") {
        email_elem.innerHTML = `
          <div style="display: flex">
            <div style="width:250px; margin: 5px;">
              <strong>${email.recipients}</strong>
            </div>
            <div style="width:250px; margin: 5px;">${email.subject}</div>
          </div>
          <div style="margin: 5px;">${email.timestamp}</div>
        `;
      };

      email_elem.addEventListener("click", function() {
        render_email(email.id, mailbox);
      });
      
      document.querySelector("#emails-view").append(email_elem);
    });
  })
  .catch(error => {
    // Handle any errors that occurred during the fetch
    console.error('Error:', error);
  });
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'none';
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

//////////////////////////////////////////////////////////////////////////////////////////////////

function sent_email(event){  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value, 
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .catch(error => {
    // Handle any errors that occurred during the fetch
    console.error('Error:', error);
  });
}
