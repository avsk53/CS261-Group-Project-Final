<template>
  <div>
    <h4>Project Information</h4>
    <b-form @submit.prevent="submitForm">
      <b-form-group label="Project Name:" label-for="project-name" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="project-name" v-model="projectName" required></b-form-input>
      </b-form-group>
      <b-form-group label="Project Start:" label-for="project-start" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-datepicker id="project-start" v-model="projectStart" required></b-form-datepicker>
      </b-form-group>
      <b-form-group label="Project End:" label-for="project-end" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-datepicker id="project-end" v-model="projectEnd" required></b-form-datepicker>
      </b-form-group>
      <b-form-group label="Project Budget (£):" label-for="project-budget" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="project-budget" type="number" v-model="projectBudget" required></b-form-input>
      </b-form-group>
      <b-form-group label="Budget Spent (£):" label-for="budget-spent" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="budget-spent" type="number" v-model="budgetSpent" required></b-form-input>
      </b-form-group>
      <b-form-group label="GitHub Link:" label-for="github-link" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="github-link" type="url" v-model="githubLink"></b-form-input>
      </b-form-group>
      <b-form-group label="Team Turnover Rate:" label-for="team-turnover" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="team-turnover" type="number" v-model="teamTurnover"></b-form-input>
      </b-form-group>
      <b-form-group label="Team Size:" label-for="team-size" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="team-size" type="number" v-model="teamSize"></b-form-input>
      </b-form-group>
      <b-form-group label="Completion:" label-for="completion" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="completion" type="range" min="0" max="100" v-model="completion"></b-form-input>
        <div style="font-size: 25px; width: 100%;">
          <p style="float: left;">0%</p>
          <p style="float: right;">100%</p>
        </div>
      </b-form-group>
      <!-- <b-form-group label="Budget (GBP):" label-for="budget" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="budget" type="number" v-model="budget"></b-form-input>
      </b-form-group> -->
      <b-form-group label="Morale:" label-for="morale" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="morale" type="range" min="0" max="100" v-model="morale"></b-form-input>
        <div style="font-size: 25px; width: 100%;">
          <b-icon-emoji-frown style="float: left;"></b-icon-emoji-frown>
          <b-icon-emoji-smile style="float: right;"></b-icon-emoji-smile>
        </div>
      </b-form-group>
      <b-form-group label="Customer Rating:" label-for="customer-rating" label-cols-md="3" label-size="sm" label-class="font-weight-bold">
        <b-form-input id="customer-rating" type="range" min="0" max="100" v-model="customerRating"></b-form-input>
        <div style="font-size: 25px; width: 100%;">
          <b-icon-emoji-frown style="float: left;"></b-icon-emoji-frown>
          <b-icon-emoji-smile style="float: right;"></b-icon-emoji-smile>
        </div>
      </b-form-group>
      <b-button type="submit" variant="primary" style="float: right;">Create Project</b-button>
    </b-form>
    <div v-if="errorMessage" class="mt-2 alert alert-danger" role="alert">{{ errorMessage }}</div>
  </div>
</template>

<script>

import { BIconEmojiSmile, BIconEmojiFrown } from 'bootstrap-vue'

import Sidebar from '~/components/Sidebar.vue'
import axios from 'axios'

export default {
  name: 'CreateProjectForm',
  props: ['loading'],
  data() {
    return {
      projectName: '',
      projectStart: null,
      projectEnd: null,
      projectBudget: 0,
      budgetSpent: 0,
      numPeople: 0,
      githubLink: '',
      teamTurnover: '',
      teamSize: '',
      completion: 0,
      customerRating: 0,
      // budget: '',
      morale: '',
      errorMessage: '',
    }
  },
  methods: {
    validateForm() {
      // Check if project name is empty
      if (!this.projectName) {
        this.errorMessage = 'Please enter a project name.'
        return false
      }
      
      // Check if start date is empty
      if (!this.projectStart) {
        this.errorMessage = 'Please enter a project start date.'
        return false
      }
      
      // Check if end date is empty
      if (!this.projectEnd) {
        this.errorMessage = 'Please enter a project end date.'
        return false
      }

      if (!this.projectBudget) {
        this.errorMessage = 'Please enter a project budget.'
        return false
      }
      
      if (!this.budgetSpent) {
        this.errorMessage = 'Please enter the amount of your budget spent.'
        return false
      }

      // Check if start date is after end date
      if (new Date(this.projectStart) > new Date(this.projectEnd)) {
        this.errorMessage = 'The project start date cannot be after the project end date.'
        return false
      }
      
      // All validation checks passed
      return true
    },
    
    submitForm() {
      // Validate the form before sending
      if (!this.validateForm()) {
        console.log('invalid information')
        return
      }
      
      // Set default values for optional inputs if not specified by user
      if (!this.githubLink) {
        this.githubLink = ''
      }
      
      if (!this.teamTurnover) {
        this.teamTurnover = 0
      }
      
      if (!this.teamSize) {
        this.teamSize = 1
      }
      
      if (!this.morale) {
        this.morale = 50
      }

      if (!this.completion) {
        this.completion = 0
      }

      if (!this.customerRating) {
        this.customerRating = 50
      }

      // if (!this.budget) {
      //   this.budget = 0
      // }

      // Build the JSON data to be sent to the server
      const data = {
        server_token: 0,
        user_id: this.$auth.user.user_id,
        form_data: {
          project_name: this.projectName,
          project_start_date: this.projectStart,
          project_end_date: this.projectEnd,
          github_url: this.githubLink,
          soft_metrics: [
            {
              metric_id: 0,
              metric_value: this.teamTurnover
            },
            {
              metric_id: 1,
              metric_value: this.customerRating
            },
            {
              metric_id: 2,
              metric_value: this.teamSize
            },
            {
              metric_id: 3,
              metric_value: this.morale
            },
            {
              metric_id: 12,
              metric_value: this.budgetSpent
            },
            {
              metric_id: 13,
              metric_value: this.completion
            },
            {
              metric_id: 15,
              metric_value: this.projectBudget
            }
          ]
        }
      }
      
      this.$root.$refs.Dashboard.busy = true;
      // Send the JSON data to the server
      axios.post('http://localhost:5555/create_project', data, {
          headers: { 
            'Content-Type': 'application/json', 
            'x-access-token': this.$auth.strategy.token.get().substr(7)
          }
        }).then(response => {
          console.log(response)
          // showCreateProjectForm = true
          // Do something with the server response
          console.log(this.$root.$refs.Dashboard.projects);
          this.$root.$refs.Dashboard.projects.push(response.data);
          console.log(this.$root.$refs.Dashboard.projects);
          this.$root.$refs.Dashboard.busy = false;
        })
        .catch(error => {
          console.log(error)
          // Handle the error
          this.$root.$refs.Dashboard.busy = false;
        })
      this.$emit('form-submitted');
        
    }
  }
}
</script>
