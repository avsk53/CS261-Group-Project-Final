<template>
    <b-container style="height: 85vh;" class="d-flex align-content-center justify-content-center flex-column">
        <b-alert
            :show="show_successful_alert"
            dismissible
            fade
            variant="success"
            @dismissed="show_successful_alert = false"
        >
            User Account Successfully created
        </b-alert>
        <b-alert
            :show="show_user_altready_exists_alert"
            dismissible
            fade
            variant="danger"
            @dismissed="show_user_altready_exists_alert = false"
        >
            User Account already exists
        </b-alert>
        <b-alert
            :show="show_failed_alert"
            dismissible
            fade
            variant="danger"
            @dismissed="show_failed_alert = false"
        >
            User Account creation failed
        </b-alert>
                
        <b-overlay :show="show" rounded="sm" class="d-flex align-content-center justify-content-center">
            <b-card class="w-50 " bg-variant="light">
                <h3 class="text-center">User Account Registration</h3>
                <b-form @submit="on_submit" @reset="on_reset">
                    <b-form-group
                        id="username_group"
                        label="Username: "
                        label-for="username_input"
                        valid-feedback="Username is valid format"
                        :invalid-feedback="username_invalidFeedback"
                        :state="username_state"
                        label-cols-sm="5"
                        label-cols-lg="3"
                        label-cols-md="4"
                        content-cols-sm
                        content-cols-lg="7"
                        
                    >
                        <b-form-input 
                            id="username_input" 
                            class="login_inputs"
                            v-model="username" 
                            :state="username_state" 
                            trim 
                            type="text"
                            required
                            placeholder="Enter a new username"
                        />
                    </b-form-group>
                    <b-form-group 
                        label="User Role:" 
                        v-slot="{ ariaDescribedby }" 
                        class="d-flex justify-content-center flex-column"
                        label-cols-sm="5"
                        label-cols-lg="3"
                        label-cols-md="4"
                        content-cols-sm
                        content-cols-lg="7"
                    >
                        <b-form-radio 
                            v-model="user_role" 
                            :aria-describedby="ariaDescribedby" 
                            name="some-radios" 
                            value="0"
                            
                        >
                            System Admin
                        </b-form-radio>
                        <b-form-radio 
                            v-model="user_role" 
                            :aria-describedby="ariaDescribedby" 
                            name="some-radios" 
                            value="1"
                        >
                            Supervisor
                        </b-form-radio>
                        <b-form-radio 
                            v-model="user_role" 
                            :aria-describedby="ariaDescribedby" 
                            name="some-radios" 
                            value="2"
                        >
                            Project Manager
                        </b-form-radio>
                    </b-form-group>
                    <b-form-group
                        id="email_group"
                        label="Email Address: "
                        label-for="email_input"
                        valid-feedback="Email address is valid format"
                        :invalid-feedback="email_invalidFeedback"
                        :state="email_state"
                        label-cols-sm="5"
                        label-cols-lg="3"
                        label-cols-md="4"
                        content-cols-sm
                        content-cols-lg="7"
                        
                    >
                        <b-form-input 
                            id="email_input" 
                            class="login_inputs"
                            v-model="email_address" 
                            :state="email_state" 
                            trim 
                            type="email"
                            required
                            placeholder="Enter your email address"
                        />
                    </b-form-group>    
                    <b-form-group
                        id="password_group"
                        label="Password: "
                        label-for="password_input"
                        valid-feedback="Password is valid"
                        :invalid-feedback="password_invalidFeedback"
                        :state="password_state"
                        label-cols-sm="5"
                        label-cols-lg="3"
                        label-cols-md="4"
                        content-cols-sm
                        content-cols-lg="7"
                        
                    >
                        <b-form-input 
                            id="password_input" 
                            class="login_inputs" 
                            v-model="password" 
                            :state="password_state" 
                            type="password" 
                            required
                            size="md"
                            placeholder="Enter the user's new password"
                        />
                    </b-form-group>
                    <div class="d-flex justify-content-center " style="gap: 10px;">
                        <b-button type="submit" variant="primary">Submit</b-button>
                        <b-button type="reset" variant="danger">Reset</b-button>
                    </div>
                    
                </b-form>
                
            </b-card>

        </b-overlay>
    </b-container>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'CreateUserAccount',

        data () { 
            return {
                show: false, 
                email_address: null, 
                password: null, 
                username: null,
                user_role: 0,
                successfullogin: false,
                show_successful_alert: false,
                show_user_altready_exists_alert: false,
                show_failed_alert: false,
            }
        }, 
        
        computed: {
            email_state() {
                return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.email_address))
            },
            email_invalidFeedback() {
                return !this.email_state ? 'Please enter a valid email address' : null
            },
            password_state() {
                return !this.password ? false : (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(this.password))
            },
            password_invalidFeedback() {
                return !this.password_state ? 'All passwords must have length at least 8 and must contain: one lowercase letter, one uppercase letter, one number and one symbol.' : null
            },
            username_state() {
                return !this.username ? false : true
            }, 
            username_invalidFeedback() {
                return !this.username_state ? 'Please enter a valid username' : null
            }
        },
        
        methods: {
            reset_data() { 
                this.email_address = null
                this.password = null
                this.username = null
                this.user_role = "0"
            }, 
            display_correct_alert(response){
                if (response.status == 200){
                    this.show_successful_alert = true
                    this.show_user_altready_exists_alert = false
                    this.show_failed_alert = false
                }else if (response.status == 402){
                    this.show_successful_alert = false
                    this.show_user_altready_exists_alert = true
                    this.show_failed_alert = false
                }else{
                    this.show_successful_alert = false
                    this.show_user_altready_exists_alert = false
                    this.show_failed_alert = true
                }
            },
            async on_submit(event) { 
                event.preventDefault()
                this.show = !this.show        
                const body = {
                    "server_token": 0, 
                    "username_created": this.username,
                    "user_role_created": this.user_role,
                    "email_created": this.email_address,
                    "password_created": this.password

                };
                axios.post('http://localhost:5555/create_user_account', JSON.stringify(body), {
                    headers: { 
                        'Content-Type': 'application/json',
                        'x-access-token': this.$auth.strategy.token.get().substr(7)
                    }
                }).then(response => {
                    this.display_correct_alert(response)
                }).catch(error => {
                    this.display_correct_alert(error.response)
                    // console.log("hello");
                });
                this.show = !this.show
                this.reset_data()
            }, 
            on_reset(event) { 
                event.preventDefault()
                this.reset_data()
            }
        }
    }
</script>

<style scoped>

</style>