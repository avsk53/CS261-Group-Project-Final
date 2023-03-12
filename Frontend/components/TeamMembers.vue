<template>
    <div class="team-information text-center">
        <div class="table-header my-4 d-flex align-items-center justify-content-between">
          <p>Team</p>
          <b-button pill variant="primary" size="sm" class="m-1" v-b-modal.assign_new_member>   
            Add Member
          </b-button>
        </div>
        <b-modal id="assign_new_member" title="Assign New Project Member" hide-footer size="lg">
            <div class="d-flex justify-content-between">
              <b-form inline class="d-flex justify-content-center align-content-center" @submit="on_submit">
                  <b-form-group id="input-group-1" label-for="input-1">
                      <b-form-input 
                        id="input-1" 
                        type="text" 
                        v-model="search_term" 
                        placeholder="Enter username or email"
                        
                      />
                  </b-form-group>
                  <b-button size="sm" @click="make_search()" variant="outline-dark">
                    <b-icon-search class="m-1"></b-icon-search>
                  </b-button>
              </b-form>
              <b-button pill variant="primary" size="sm" class="m-1" v-b-modal.create_new_developer>
                Create New Developer  
              </b-button>
            </div>
            <b-modal id="create_new_developer" title="Create New Developer" hide-footer size="sm">
              <b-form
                class="d-flex justify-content-center align-content-center flex-column"
                @submit="create_dev"
              >
                <b-form-group
                  id="dev-input-group-1"
                  label-for="dev-input-1"
                  label="Username: "
                  valid-feedback=""
                  :invalid-feedback="username_invalidFeedback"
                  :state="username_state"
                >
                  <b-form-input
                    id="dev-input-1"
                    type="text"
                    v-model="new_dev_username"
                    placeholder="Enter developer username"
                    :state="username_state"
                  />
                </b-form-group>
                <b-form-group
                  id="dev-input-group-2"
                  label-for="dev-input-2"
                  label="Email Address: "
                  valid-feedback="Email address is valid format"
                  :invalid-feedback="email_invalidFeedback"
                  :state="email_state"
                >
                  <b-form-input
                    id="dev-input-2"
                    type="email"
                    v-model="new_dev_email"
                    :state="email_state" 
                    trim 
                    placeholder="Enter developer email"
                  />
                </b-form-group>
                <div class="d-flex justify-content-center " style="gap: 10px;">
                  <b-button type="submit" variant="primary" :disabled="!email_state || !username_state">Submit</b-button>
                  <b-button type="reset" variant="danger">Reset</b-button>
                </div>
              </b-form>
            </b-modal>
            <b-table 
              striped hover 
              sticky-header="40vh"
              :items="searched_developers" 
              :fields="searched_developer_fields" 
              class="m-1 w-100" 
              style="height: 40vh;"
              empty-text="No results found"
              show-empty
              outline
              :busy="this.table_loading"
            >
                <template #cell(user_id)="data">
                    <b-button size="sm" @click="add_member(data.item)">
                        <b-icon-plus-circle-fill></b-icon-plus-circle-fill>
                    </b-button>
                </template>
                <template #table-busy>
                  <div class="text-center text-danger my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Loading...</strong>
                  </div>
                </template>
            </b-table>
        </b-modal>
        <b-table 
          responsive 
          striped hover 
          :items="project_data.team_members" 
          :fields="current_developer_fields" 
          class="m-1"
          sticky-header="250px"
        >
          <template #cell(user_id)="data">
              <b-button size="sm" @click="remove_member(data.item)">
                  <b-icon-dash-circle-fill></b-icon-dash-circle-fill>
              </b-button>
          </template>

        </b-table>
    </div>
  </template>
  
<script>
  
  import axios from 'axios'
  import {BIconDashCircleFill, BIconPlusCircleFill } from 'bootstrap-vue'

  export default {
    name: 'TeamMembers',
    props: [
      'project_data'
    ],
    data() {
      return {
        current_developer_fields: [
          {'key': 'user_id', 'label': 'Remove'},
          {'key': 'username', 'label': 'Username', sortable: true}, 
          {'key': 'role', 'label': 'Role Description', sortable: true}
        ], 
        searched_developer_fields: [
          {'key': 'user_id', 'label': 'Add'},
          {'key': 'username', 'label': 'Username', sortable: true},
          {'key': 'email', 'label': 'Email', sortable: true}
        ],
        show_assign_new_member: false,
        table_loading: false,
        searched_developers: [],
        search_term: '', 
        new_dev_username: '',
        new_dev_email: ''
      }
    },
    computed: {
      email_state() {
        return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.new_dev_email))
      },
      email_invalidFeedback() {
        return !this.email_state ? 'Please enter a valid email address' : null
      },
      username_state() {
        return (this.new_dev_username.length > 0)
      },
      username_invalidFeedback() {
        return !this.username_state ? 'Please enter a username' : null
      }
    },
    methods: {
      remove_member(user) {   
        const request_data = {
          "server_token": 0,
          "user_id": user.user_id, 
          "email" : user.email,
          "project_id": this.project_data.project_id
        }
        axios.post("http://localhost:5555/remove_developer", JSON.stringify(request_data), 
        {
          headers: {
            'Content-Type': 'application/json', 
            'x-access-token': this.$auth.strategy.token.get().substr(7)
          }
        }).then(response => {
          this.project_data.team_members = response.data.team_members
          this.project_data.current_metrics[2].value -= 1
          if (response.status == 200) {
            this.$bvToast.toast('Developer removed from project', {
              title: 'Success',
              variant: 'success',
              solid: true
            })
          }
        }).catch(error => {
          if (error.response.status == 400){
            this.$bvToast.toast('Developer is not already assigned to this project', {
              title: 'Error',
              variant: 'danger',
              solid: true
            })
          }else{
            this.$bvToast.toast('Error removing developer from project', {
              title: 'Error',
              variant: 'danger',
              solid: true
            })
          }
        })
      }, 
      add_member(user) {
        const request_data = {
          "server_token": 0,
          "user_id": user.user_id, 
          "email" : user.email,
          "project_id": this.project_data.project_id
        }
        axios.post("http://localhost:5555/assign_developer", JSON.stringify(request_data), 
        {
          headers: {
            'Content-Type': 'application/json', 
            'x-access-token': this.$auth.strategy.token.get().substr(7)
          }
        }).then(response => {   
          this.project_data.team_members = response.data.team_members
          this.project_data.current_metrics[2].value += 1
          if (response.status == 200) {
            this.$bvToast.toast('Developer added to project', {
              title: 'Success',
              variant: 'success',
              solid: true
            })
          }
        }).catch(error => {
          if (error.response.status == 400) {
            this.$bvToast.toast('Developer already assigned to project', {
              title: 'Error',
              variant: 'danger',
              solid: true
            })
          }else{
            this.$bvToast.toast('Error adding developer to project', {
              title: 'Error',
              variant: 'danger',
              solid: true
            })
          }
        })
      },
      on_submit(evt) {
        evt.preventDefault()
        this.make_search()
      },
      make_search(){
        this.table_loading = true
        console.log(this.search_term)
        const request_data = {
          "server_token": 0,
          "substring": this.search_term
        }
        axios.post('http://localhost:5555/search_user',JSON.stringify(request_data), 
        {
          headers: {
            'Content-Type': 'application/json', 
            'x-access-token': this.$auth.strategy.token.get().substr(7)
          }
        }).then(response => {
          this.searched_developers = response.data.users
        }).catch(error => {
          this.$bvToast.toast('Error searching for developers', {
            title: 'Error',
            variant: 'danger',
            solid: true
          })
        })
        this.table_loading = false
        console.log(this.searched_developers)
      }, 
      create_dev(event){
        event.preventDefault()
        const request_data = {
          "server_token": 0,
          "username": this.new_dev_username,
          "email": this.new_dev_email
        }
        axios.post('http://localhost:5555/create_developer',JSON.stringify(request_data), 
        {
          headers: {
            'Content-Type': 'application/json', 
            'x-access-token': this.$auth.strategy.token.get().substr(7)
          }
        }).then(response => {
          if (response.status == 200) {
            this.$bvToast.toast('Developer created successfully', {
              title: 'Success',
              variant: 'success',
              solid: true
            })
          }
          // Resetting the form
          this.new_dev_email = ''
          this.new_dev_username = ''
        }).catch(error => {
          if (error.response.status == 402) {
            this.$bvToast.toast('Developer already exists', {
              title: 'Error',
              variant: 'danger',
              solid: true
            })
          }
          else {
            this.$bvToast.toast('Error creating developer', {
              title: 'Error',
              variant: 'danger',
              solid: true
            })
          }
        })
        
      }    
    }
  }
</script>
  
<style>
  .table-header{
    padding: 10px 30px;
    border-bottom: 1px solid rgb(151,196,235);
    margin-bottom: 20px !important;
    margin-top:0 !important;
  }

  .table-header p{
    margin-bottom: 0;
    font-size: 18px;
    font-weight: bold;
  }

    .team-information {
      width: 25%;
      background-color: #f5f5f5;
      border-radius: 15px;
      margin: 10px;
      padding: 5px;
    }
    
    .table-data {
      font-size: 14px;
      font-weight: bold;
    }
    
    .project-name {
      font-size: 16px;
      font-weight: bold;
    }
    
    .project-risk {
      font-size: 12px;
      color: #fff;
      text-align: center;
      padding: 4px 8px;
      border-radius: 4px;
    }
    
    .b-table-sticky-header > .table.b-table > thead > tr > th {
      position: sticky !important;
    }
  </style>