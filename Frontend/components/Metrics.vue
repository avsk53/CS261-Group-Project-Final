<template>
  <div class="table-wrapper">
      <div class="table-header my-4 d-flex align-items-center justify-content-between">
        <p>Current Metrics</p>
        <b-button pill variant="outline-success" size="sm" @click="updateForm()">{{update?'Complete':'Update'}}</b-button>
      </div>
      <b-table 
        sticky-header="250px" 
        head-variant="light" 
        class="table-data" 
        bordered 
        :fields="fields" 
        hover 
        :items="this.table_data"
        style="width: 324px"
        >
          <template #cell(value)="data">
            <div v-if="!update || data.item.metric_type!=0">{{data.item.value}}</div>
            <b-form-input size="sm" type="text" v-model="data.item.value" v-else></b-form-input>
          </template>
      </b-table>
  </div>
</template>

<script>
  import { BTable, BFormInput, BButton } from 'bootstrap-vue'
  import axios from 'axios'

  export default{
    name:'Metrics',
    props:[
      'projectData'
    ],
    data(){
      return{
        fields: [
          {
            key:'metric_id',
            label:'ID',
            class: 'text-center'
          },
          'metric_description',
          'value',
        ],
        update:false,
        table_data: []
      }
    }, 
    watch : {
      projectData: function(){
        this.table_data = this.projectData.current_metrics.sort((a,b) => (a.metric_type > b.metric_type) ? 1 : (b.metric_type > a.metric_type) ? -1 : 0)
      }
    },
    methods: {
      updateForm(){
        if (this.update){
          let request_body = {
            "server_token": 0,
            "project_id": this.projectData.project_id,
            "updated_metrics": this.projectData.current_metrics
          }
          
          axios.post('http://localhost:5555/update_soft_metrics', JSON.stringify(request_body), 
          {
            headers: {
              'Content-Type': 'application/json', 
              'x-access-token': this.$auth.strategy.token.get().substr(7)
            }
          }).then(response => {
            console.log(response)
            for (let metric in response.data.metrics){
              if (metric.metric_type==0){
                delete this.projectData.current_metrics[metric.metric_id]
                this.projectData.current_metrics.push(metric)
              }
            }
          }).catch(error => {
            console.log(error)
          })
        }
        this.update=!this.update;
      }, 
    }
  }
</script>

<style scoped>
  .table-wrapper{
    max-width: 40%;
    min-width: 350px;
    border-radius: 20px;
    padding: 10px;
    margin: 10px;
    background-color: #f5f5f5;
  }
  .table-header{
    padding: 10px 30px;
    border-bottom: 1px solid rgb(151,196,235);
    margin-bottom: 20px !important;
    margin-top:0 !important;
  }
  .table-wrapper .table-bordered th, .table-wrapper .table-bordered td{
    border-color:rgb(151,196,235);
  }
  .table-data thead th div{
    border-bottom: 1px solid;
  }
  .table-header p{
    margin-bottom: 0;
    font-size: 18px;
    font-weight: bold;
  }
  .table-data{
    padding:0 10px;
  }
  
  .b-table-sticky-header .table.b-table > thead > tr > th{
    top: -1px;
  }

</style>