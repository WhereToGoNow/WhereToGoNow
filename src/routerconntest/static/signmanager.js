class SignManager {
    constructor(args) {
        this.idContainer = $(args.idContainer);
        this.passwordContainer = $(args.passwordContainer);

        this.toggleButton = $(args.toggleButton);
        this.signUpButton = $(args.signUpButton);
        this.signInButton = $(args.signInButton);
        this.signOutButton = $(args.signOutButton);

        this.resultText = $(args.resultText)

        this.id = '';
        this.password = '';

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

        this.id = inputs.id;
        this.password = inputs.password;
        this.disableToggle();
    }

    signIn() {
        var inputs = this.readInputs();

        if (inputs == null) {
            return;
        }

        this.id = inputs.id;
        this.password = inputs.password;
        this.disableToggle();
    }

    signOut() {
        this.enableToggle();
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
            this.resultText.css('color', 'red').text(
                'Id and password should be unempty!');
            return null;
        } else {
            return {id: id, password: password};
        }
    }
}
