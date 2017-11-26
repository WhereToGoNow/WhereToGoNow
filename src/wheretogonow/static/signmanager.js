/*
 * Class for signing up & signing in & signing out.
 * Use this module *after* loading js-sha256(static/libs/sha256.min.js).
 */

class SignManager {
    constructor(args) {
        this.formContainer = $(args.formContainer);
        this.idContainer = $(args.idContainer);
        this.passwordContainer = $(args.passwordContainer);

        this.signUpButton = $(args.signUpButton);
        this.signInButton = $(args.signInButton);
        this.signOutButton = $(args.signOutButton);

        this.resultText = $(args.resultText)

        // true when user is signed-in currently
        this.signed = false;

        // store the current (user) id for future use
        this.currId = '';

        // bind the methods to the buttons
        this.signUpButton.click(() => {this.signUp()});
        this.signInButton.click(() => {this.signIn()});
        this.signOutButton.click(() => {this.signOut()});

        // at first, disable signOutButton and show formContainer
        this.signOutButton.disabled = true;
        this.formContainer.show();
    }

    signUp() {
        var inputs = this.readInputs();

        if (inputs == null) {
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/sign-up',
            data: JSON.stringify({
                id: inputs.id,
                password: this.encryptToHex(inputs.password)
            }),
            success: (data) => {
                if (data.success) {
                    this.signed = true;
                    this.currId = inputs.id;
                    this.signOutButton.attr('disabled', false);
                    this.formContainer.hide();
                } else {
                    this.resultText.text(data.msg);
                }
            },
            contentType: 'application/json',
            dataType: 'json'
        });
    }

    signIn() {
        var inputs = this.readInputs();

        if (inputs == null) {
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/sign-in',
            data: JSON.stringify({
                id: inputs.id,
                password: this.encryptToHex(inputs.password)
            }),
            success: (data) => {
                if (data.success) {
                    this.signed = true;
                    this.currId = inputs.id;
                    this.signOutButton.attr('disabled', false);
                    this.formContainer.hide();
                } else {
                    this.resultText.text(data.msg);
                }
            },
            contentType: 'application/json',
            dataType: 'json'
        });
    }

    signOut() {
        $.ajax({
            type: 'POST',
            url: '/sign-out',
            data: '',
            success: (data) => {
                if (data.success) {
                    this.signed = false;
                    this.currId = '';

                    // reload the page
                    // XXX: Is there a better method???
                    // this.signOutButton.disabled = true;
                    // this.formContainer.show();
                    location.reload();
                } else {
                    // do nothing
                }
            },
            contentType: 'application/json',
            dataType: 'json'
        });
    }

    readInputs() {
        var id = this.idContainer.val();
        var password = this.passwordContainer.val();

        // check whether the inputs are valid
        if (!id || !password || !id.length || !password.length) {
            this.resultText.text('Id and password should be unempty!');
            return null;
        } else {
            return {id: id, password: password};
        }
    }

    encryptToHex(str) {
        var hash = sha256.create();
        hash.update(str);
        return hash.hex();
    }
}
