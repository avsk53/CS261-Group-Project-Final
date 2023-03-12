<template>
  <div class="project-information text-center">
    <div class="table-header my-4 d-flex align-items-center justify-content-between">
        <p>Project Information</p>
      </div>
    <table class="table table-hover table-sm" style="width: 270px">
      <tbody>
        <tr class="d-flex">
          <th class="col-4 fs-1" scope="row">
            <b-icon-person-circle></b-icon-person-circle>
            Manager
          </th>
          <td class="col-8 align-bottom table-data">{{ projectData.project_manager_name }}</td>
        </tr>
        <tr class="d-flex">
          <th class="col-4 fs-3" scope="row">
            <b-icon-github></b-icon-github>
            GitHub
          </th>
          <td class="col-8 align-bottom"><a class="link-info" style="word-wrap: break-word; overflow-wrap: break-word;" :href="projectData.github_url">{{ projectData.github_url }}</a></td>
        </tr>
        <tr class="d-flex">
          <th class="col-4 fs-3" scope="row">
            <b-icon-calendar-plus></b-icon-calendar-plus>
            Started
          </th>
          <td class="col-8 align-bottom table-data">
            <b-form-datepicker
              size="sm"
              v-model="projectData.project_start_date"
              @input="event => updateStartDate()"
              :max="projectData.project_end_date"
              :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }">
            </b-form-datepicker>
          </td>
        </tr>
        <tr class="d-flex">
          <th class="col-4 fs-3" scope="row">
            <b-icon-calendar-check></b-icon-calendar-check>
            Deadline
          </th>
          <td class="col-8 align-bottom table-data">
            <b-form-datepicker
              size="sm"
              v-model="projectData.project_end_date"
              @input="event => updateEndDate()"
              :min="projectData.project_start_date"
              :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }">
            </b-form-datepicker>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="project-risk project-name" :class="projectData?.recent_evaluation?.evaluation_label.replace(' ', '')">
      {{ projectData?.recent_evaluation?.evaluation_label }}
    </div>
    <br>
    <b-button variant="primary" size="sm"
      @click="evaluate"> 
      <b-icon-arrow-clockwise></b-icon-arrow-clockwise>
      Update Evaluation
    </b-button>
  </div>
</template>

<script>

import axios from 'axios'
import { BIconArrowClockwise, BIconPersonCircle, BIconGithub, BIconCalendarPlus, BIconCalendarCheck} from 'bootstrap-vue'

export default {
  name: 'ProjectInformation',
  props: [
    'projectData'
  ],
  methods: {
    evaluate() {
      this.$root.$refs.Dashboard.evaluate(this.projectData.project_id);
    },

    updateStartDate() {
      const body = {
        "server_token": 0, 
        "project_id": this.projectData.project_id,
        "attribute": 'start_date',
        "new_value": this.projectData.project_start_date,
      };
      axios.post('http://localhost:5555/update_project_info', JSON.stringify(body), {
        headers: {
          'Content-Type': 'application/json', 
          'x-access-token': this.$auth.strategy.token.get().substr(7)
        }
      });
    },
    updateEndDate() {
      const body = {
        "server_token": 0, 
        "project_id": this.projectData.project_id,
        "attribute": 'end_date',
        "new_value": this.projectData.project_end_date,
      };
      axios.post('http://localhost:5555/update_project_info', JSON.stringify(body), {
        headers: {
          'Content-Type': 'application/json', 
          'x-access-token': this.$auth.strategy.token.get().substr(7)
        }
      });
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

  .project-information {
    width: 30%;
    min-width: 300px;
    background-color: #f5f5f5;
    border-radius: 15px;
    margin: 15px;
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
  
  .Failing{
    background-color: #ff4d4f;
  }
  
  .AtRisk {
    background-color: #faad14;
  }
  
  .ShowingSymptoms{
    background-color: #8314fa;
  }
  
  .Successful {
    background-color: #52c41a;
  }
</style>