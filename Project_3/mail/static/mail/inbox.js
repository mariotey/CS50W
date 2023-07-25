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

function load_mailbox(mailbox) {
  // three possible mailboxes: inbox, sent, archive

  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(`GET /emails/${mailbox}`);

      emails.forEach(email => {
        const email_elem = document.createElement("div");
        email_elem.style.cssText =`
          display: flex;  
          border: solid black 2px;
          justify-content: space-between;

        `;
        email_elem.innerHTML = `
          <div style="display: flex">
            <div style="width:250px; margin: 5px;">
              <strong>${email.recipients}</strong>
            </div>
            <div style="width:250px; margin: 5px;">${email.subject}</div>
          </div>
          <div style="margin: 5px;">${email.timestamp}</div>
        `;

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
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

//////////////////////////////////////////////////////////////////////////////////////////////////

function sent_email(event){

  // Post email to API route
  fetch('/emails' , {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log("POST /emails");
      console.log(result);
  })
  .catch(error => {
      // Handle any errors that occurred during the fetch
      console.error('Error:', error);
  });
}
