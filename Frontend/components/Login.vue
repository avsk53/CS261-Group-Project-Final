<template>  
    <b-container>
        <b-overlay :show="show" rounded="sm" class="d-flex align-content-center justify-content-center">
            <b-card class="w-50" bg-variant="light" text-variant="black">
                <b-form @submit="on_submit" @reset="on_reset">
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
                        valid-feedback="Password is of valid length"
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
                            placeholder="Enter your password"
                        />
                    </b-form-group>
                    <div class="d-flex justify-content-center " style="gap: 10px;">
                        <b-button type="submit" variant="primary" :disabled="!email_state || !password_state">Submit</b-button>
                        <b-button type="reset" variant="danger">Reset</b-button>
                    </div>
                    <div class="text-center" style="color: red; margin-top:5px;" v-text="error"></div>
                </b-form>
            </b-card>
        </b-overlay>
    </b-container>
</template>

<script>
    // import axios from 'axios'
    import { mapGetters } from 'vuex'

    export default {

        data () { 
            return {
                show: false, 
                email_address: null, 
                password: null, 
                successfullogin: false,
                error: ''
            }
        }, 

        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser']),
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
            }
        },

        methods: {
            async on_submit(event) { 
                event.preventDefault()
                this.show = !this.show        
                const login = {'server_token': 0, 'email': this.email_address, 'password': this.password}
                try {
                    const response = await this.$auth.loginWith('local', { data: login})
                    this.$auth.setUser(response.data.user)
                    console.log(this.$auth.user.role_id)
                    if (this.$auth.user.role_id === 0) {
                        console.log('admin')
                        this.$router.push('/sys_admin')
                    }else{
                        console.log('user')
                        this.$router.push('/dashboard')
                    }
                } catch (err) {
                    this.error = "Invalid username or password.";
                }
                this.show = !this.show
            }, 
            on_reset(event) { 
                this.email_address = null
                this.password = null
                this.error = ""
            }
        }
    }
</script>

<style>
    .login_inputs {
        height: 40px;
        font-size: 13px;
    }
    #login_component {
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
</style>
