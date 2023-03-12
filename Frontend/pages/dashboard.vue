<template>
  <div class="dashboard">
    <sidebar :projects="projects" :loading="busy"/>
    <b-overlay :show="busy" class="main-content">
      <template #overlay>
        <div class="d-flex align-items-center">
          <b-spinner small type="grow" variant="secondary"></b-spinner>
          <b-spinner type="grow" variant="dark"></b-spinner>
          <b-spinner small type="grow" variant="secondary"></b-spinner>
          <!-- We add an SR only text for screen readers -->
          <span class="sr-only">Please wait...</span>
        </div>
      </template>
      <div class="text-center" style="width:100%;">
        <h3>Project Overview: {{ projectData.project_name }}</h3>
      </div>
      <!-- your main content here -->
      <div class="d-flex flex-wrap justify-content-center">
        <ProjectInformation :projectData="projectData"/>
        <TeamMembers :project_data="projectData"/>
        <Metrics :projectData="projectData"/>
        <EvaluationHistory :projectData="projectData"/>
        <Improve :project_data="projectData"/>
      </div>  
    </b-overlay>
  </div>
</template>

<script>
  import axios from 'axios'
  import ProjectInformation from '~/components/ProjectInformation.vue'
  import TeamMembers from '~/components/TeamMembers.vue'
  import Metrics from '~/components/Metrics.vue'
  import Improve from '~/components/Improve.vue'
  import Sidebar from '~/components/Sidebar.vue'
  import CreateProjectForm from '~/components/CreateProjectForm.vue';
  import EvaluationHistory from '~/components/EvaluationHistory.vue';

  import { mapGetters } from 'vuex'

  export default {
    name: 'DashboardPage',
    layout: 'default',
    middleware: ['authorization'],
    data() {
      return {
        projectData: {},
        team_members: [],
        projects: [], 
        busy: false,
      }
    },
    components: {
      Sidebar,
      ProjectInformation,
      EvaluationHistory
    },
    methods: {
      logout() {
        this.$auth.logout()
        this.$router.push('/')
      },

      evaluate(project_id) {
        this.busy = true;
        const body = {
            "server_token": 0, 
            "project_id": project_id,
        };
        axios.post('http://localhost:5555/request_evaluation', JSON.stringify(body), {
            headers: { 
                'Content-Type': 'application/json',
                'x-access-token': this.$auth.strategy.token.get().substr(7)
            }
        }).then(response => {
            this.selectProject(project_id);
            this.busy = false;
        }).catch(error => {
            console.log(error);
            this.busy = false;
        });
      },

      selectProject(project_id) {
        this.busy = true;
        const params = new URLSearchParams();
        params.append('project_id', project_id);
        params.append('server_token', '0');
        // console.log(params.toString()); // add this line
        axios.post('http://localhost:5555/get_project_specific', params, {
            headers: { 
              'Content-Type': 'application/x-www-form-urlencoded', 
              'x-access-token': this.$auth.strategy.token.get().substr(7)
            }
        }).then(response => {
          this.projectData = response.data;
          this.projectData.project_start_date = new Date(this.projectData.project_start_date);
          this.projectData.project_end_date = new Date(this.projectData.project_end_date);
          
          this.projectData.project_start_date = this.projectData.project_start_date.toISOString().split('T')[0];
          this.projectData.project_end_date = this.projectData.project_end_date.toISOString().split('T')[0];
          for (var i=0; i < this.projects.length; i++) {
            if (this.projects[i].project_id == project_id) {
              console.log(this.projects);
              console.log("SETTING");
              var proj = this.projects[i];
              proj.recent_evaluation_label = this.projectData?.recent_evaluation?.evaluation_label;
              this.projects.splice(i, 1, proj);
              console.log("SET");
              console.log(this.projects);
              console.log(this.projectData?.recent_evaluation?.evaluation_label);
              console.log(this.projects[i].recent_evaluation_label);
              
            }
          }
          this.busy = false;
        }).catch(error => {
            // console.log(error);
            this.busy = false;
        });
        console.log(this.projectData);
      }
    },

    created() {
        this.$root.$refs.Dashboard = this;
    },

    mounted() {
      const params = new URLSearchParams();
      params.append('user_id', this.$auth.user.user_id);
      params.append('server_token', '0');
      axios.post('http://localhost:5555/get_list_of_project', params, {
            headers: { 
              'Content-Type': 'application/x-www-form-urlencoded', 
              'x-access-token': this.$auth.strategy.token.get().substr(7)
            }
        })
        .then(response => {
          this.projects = response.data;
          if (this.projects.length > 0) {
            this.selectProject(this.projects[0].project_id);
          }
        })
        .catch(error => {
          // console.log(error);
        });
    },
  }
</script>

<style>
.dashboard {
  display: flex;
  min-height: 90vh;
  max-height: 90vh;
  height: 90vh;
}

.main-content {
  flex: 5;
  background-color: lightgray;
  overflow-y: auto;
  overflow-x: hidden;
  /* your main content styles here */
}
</style>