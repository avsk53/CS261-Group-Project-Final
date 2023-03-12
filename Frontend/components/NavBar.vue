<template>
	<b-navbar variant="dark" type="light" style="max-height: 5vh; min-height:5vh;">
		<b-navbar-brand to="/dashboard" class="text-light">Software Tracker</b-navbar-brand>
		<b-navbar-nav>
			<b-dropdown v-if="this.$auth.user.role_id=='1'" text="Navigation" size="sm" variant="dark">
				<b-dropdown-item to="/dashboard">Dashboard</b-dropdown-item>
				<b-dropdown-item to="/supervisor">Team Management</b-dropdown-item>
			</b-dropdown>
		</b-navbar-nav>
		<b-navbar-nav class="ml-auto">
			
			<b-nav-text>
				<b-button pill variant="primary" size="sm" v-b-modal.modal-change-password class="mr-2">Change Password</b-button>
			</b-nav-text>
			<b-nav-text>
				<b-button pill variant="primary" size="sm" class="mr-2" @click="$bvToast.show('user_info')">User</b-button>
			</b-nav-text>
			<b-nav-text>
				<b-button pill variant="primary" size="sm" @click="logout">Logout</b-button>
			</b-nav-text>
		</b-navbar-nav>
		<b-modal id="modal-change-password" ref="modal" title="Change Password" @show="resetModal" @hidden="resetModal" hide-footer>
			<b-form ref="form" @submit="on_submit" @reset="on_reset">
					<b-form-group
						id="current_password_group"
						label="Current Password: "
						valid-feedback="Current Password is valid"
						:invalid-feedback="current_password_invalidFeedback"
						:state="current_password_rules"
					>
						<div class="password-style">
							<b-form-input  
								placeholder="Current Password" 
								:type="show_current_password?'text':'password'" 
								v-model="form.currentPassword" 
								required
								:state="current_password_rules"
							/>
							<b-icon-eye
								@click="show_current_password = !show_current_password" 
								v-show="!show_current_password" 
								class="password-icon mr-4"
							/>
							<b-icon-eye-slash 
								@click="show_current_password = !show_current_password" 
								v-show="show_current_password" 
								class="password-icon mr-4"
							/>
						</div>
					</b-form-group>
					<b-form-group
						id="new_password_group"
						label="New Password: "
						valid-feedback="New Password is valid"
						:invalid-feedback="new_password_invalidFeedback"
						:state="new_password_rules"
					>
						<div class="password-style">
						<b-form-input  
							placeholder="New Password" 
							:type="showPassword?'text':'password'" 
							v-model="form.newPassword" 
							required
							:state="new_password_rules"
						/>
						<b-icon-eye
							@click="showPassword = !showPassword" 
							v-show="!showPassword" 
							class="password-icon mr-4"
						/>
						<b-icon-eye-slash 
							@click="showPassword = !showPassword" 
							v-show="showPassword" 
							class="password-icon mr-4"
						/>
						</div>
					</b-form-group>

				<b-form-group
					id="confirm_password_group"
					label="Confirm Password: "
					valid-feedback="Both passwords are same"
					:invalid-feedback="confirm_password_invalidFeedback"
					:state="confirm_password_rules"
				>		
					<div class="password-style">
						<b-form-input
							placeholder="Confirm New Password" 
							:type="showConfirmPassword?'text':'password'" 
							v-model="form.confirmPassword" 
							required
							:state="confirm_password_rules"
						/>
						<b-icon-eye 
							@click="showConfirmPassword = !showConfirmPassword" 
							v-show="!showConfirmPassword" 
							class="password-icon mr-4"
						/>
					
						<b-icon-eye-slash 
							@click="showConfirmPassword = !showConfirmPassword" 
							v-show="showConfirmPassword" 
							class="password-icon mr-4"
						/>
					</div>
				</b-form-group>
				<div class="text-right">
					<b-button pill variant="primary" type="submit">Submit</b-button>
					<b-button pill variant="warning" type="reset">Reset</b-button>
				</div>	
			</b-form>
		</b-modal>
		<b-toast 
			id="user_info" 
			title="User Info"
			solid
			toaster="b-toaster-top-right"
			no-auto-hide
			variant="info"
		>
			Username : {{ this.$auth.user.username }} <br>
			User ID : {{ this.$auth.user.user_id }} <br>
			Email : {{ this.$auth.user.email }} <br>
			Role ID : {{ this.$auth.user.role_id }} <br>
			Role : {{ this.$auth.user.role_desc }} 
		</b-toast>
	</b-navbar>
</template>

<script>
	import { 
		BNavbar, 
		BNavbarBrand, 
		BNavbarNav, 
		BNavText, 
		BButton, 
		BModal, 
		BForm, 
		BFormGroup, 
		BFormInput, 
		BIconEye, 
		BIconEyeSlash 
	} from 'bootstrap-vue'
	import axios from 'axios'

	export default {
		data() {
			return {
				form: {
					currentPassword: '',
					newPassword: '',
          			confirmPassword:'',
				},
        		showPassword:false,
       			showConfirmPassword:false,
				show_current_password:false, 
			}
		},
		computed: {
			new_password_rules(){
				return /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F])[\da-zA-Z\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F]{8,}$/.test(this.form.newPassword)
			}, 
			new_password_invalidFeedback(){
				return this.new_password_rules ? 'New Password is valid' : 'The password has to be at least 8 characters long and contains an uppercase letter and a lower case letter, contains a number and contains a symbol.'
			},
			confirm_password_rules(){
				return this.form.newPassword === this.form.confirmPassword && this.form.newPassword !== ''
			},
			confirm_password_invalidFeedback(){
				return this.confirm_password_rules ? 'Confirm Password is valid' : 'Passwords do not match or is empty'
			}, 
			current_password_rules(){
				return (!this.form.currentPassword) ? false : true
			},
			current_password_invalidFeedback(){
				return this.current_password_rules ? 'Current Password is valid' : 'Current Password is required'
			},
		},
		methods: {
			logout() {
				axios.post('http://localhost:5555/logout',JSON.stringify({"server_token": 0}), {
					headers: { 
  				        'Content-Type': 'application/json', 
  				        'x-access-token': this.$auth.strategy.token.get().substr(7)
  				      }
				}).then(response => {
					this.$auth.logout()
					this.$router.push('/')
				}).catch(error => {
					this.$bvToast.toast('Logout Failed!',{
						title: 'Error',
						toaster: 'b-toaster-top-center',
						variant: 'danger',
						solid: true
					})
				})
			}, 
			resetModal() {
				this.form = {
					currentPassword: '',
					newPassword: '',
          			confirmPassword:''
				}
				
			},
			on_reset(event){
				event.preventDefault()
				this.resetModal()
			},
			on_submit(event){
				event.preventDefault()
				const params = new URLSearchParams();
  				params.append('user_id', this.$auth.user.user_id);
  				params.append('server_token', '0');
				params.append('current_password', this.form.currentPassword);
				params.append('new_password', this.form.newPassword);
  				axios.post('http://localhost:5555/change_password', params, {
  				      headers: { 
  				        'Content-Type': 'application/x-www-form-urlencoded', 
  				        'x-access-token': this.$auth.strategy.token.get().substr(7)
  				      }
  				}).then(response => {
  				    this.projects = response.data;
					this.$bvModal.hide('modal-change-password')
					this.$bvToast.toast('Reset Successfully!',{
				  		title: 'Reminder',
				  		toaster: 'b-toaster-top-center',
				  		variant: 'success',
				  		solid: true
					})
  				}).catch(error => {
					if (error.response.status === 402) {
						this.$bvToast.toast('Current Password is incorrect!',{
							title: 'Reminder',
							toaster: 'b-toaster-top-center',
							variant: 'danger',
							solid: true
						})
					}else {
						this.$bvModal.hide('modal-change-password')
						this.$bvToast.toast('Reset Failed!',{
							title: 'Reminder',
							toaster: 'b-toaster-top-center',
							variant: 'danger',
							solid: true
						})

					}
  				});	
			},
		}
	}
</script>

<style scoped>
  .password-style{
    position: relative;
  }

  .password-style input{
    padding-right: 50px;
  }
  .password-style .password-icon{
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
  }

</style>