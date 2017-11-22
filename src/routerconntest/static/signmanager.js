/*
 * Class for signing up & signing in & signing out.
 * Use this module *after* loading js-sha256(static/libs/sha256.min.js).
 */

class SignManager {
    constructor(args) {
        this.idContainer = $(args.idContainer);
        this.passwordContainer = $(args.passwordContainer);

        this.toggleButton = $(args.toggleButton);
        this.signUpButton = $(args.signUpButton);
        this.signInButton = $(args.signInButton);
        this.signOutButton = $(args.signOutButton);

        this.resultText = $(args.resultText)

        this.onSignUp = args.onSignUp;
        this.onSignIn = args.onSignIn;
        this.onSignOut = args.onSignOut;

        // true when user is signed-in currently
        this.signed = false;

        // store the current (user) id for future use
        this.currId = '';

        /*
         * XXX: Binding the methods directly (.click(this.signUp))
         * gives TypeError. Why???
         */
        this.signUpButton.click(() => {this.signUp()});
        this.signInButton.click(() => {this.signIn()});
        this.signOutButton.click(() => {this.signOut()});

        this.enableToggle();
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
                    this.disableToggle();
                    this.onSignUp(this.currId);
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
                    this.disableToggle();
                    this.onSignIn(this.currId);
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
                    this.enableToggle();
                    this.onSignOut(this.currId);
                    this.currId = '';
                } else {
                    // do nothing
                }
            },
            contentType: 'application/json',
            dataType: 'json'
        });
    }

    /* Enable the user to sign up & sign in. */
    enableToggle() {
        // erase resultText
        this.resultText.empty();

        this.signOutButton.hide();
        this.toggleButton.show();
    }

    /* Disable the user to sign up & sign in. */
    disableToggle() {
        // collapse the panel if it is still open
        $('.collapse').collapse('hide');

        this.toggleButton.hide();
        this.signOutButton.show();
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
