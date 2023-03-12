<template>
  <div class="table-wrapper">
      <div class="table-header my-4 d-flex align-items-center justify-content-between">
        <p>Targets for Improvement</p>
      </div>
      <b-table 
        sticky-header="200px" 
        head-variant="light" 
        class="table-data" 
        bordered 
        :fields="fields" 
        hover 
        responsive
        :items="this.table_data"
      >
        <template #cell(current_value)="data">
          <div style="text-align: right;">
            {{data.item.current_value}} <b-icon-arrow-right></b-icon-arrow-right>
          </div>
        </template>
      </b-table>
  </div>
</template>

<script>
  import { BIconArrowRight } from 'bootstrap-vue'

  export default{
    name:'Improve',

    props:[
      'project_data'
    ],
    data(){
      return{
        fields: [
          {
            key:'metric_id',
            label:'ID',
            class: 'text-center'
          },
          {
            key:'metric_description',
            label:'Metric Description',
          },
          {
            key:'current_value',
            label:'Current Value',
          },
          {
            key:'value',
            label:'Target Value',
          },
        ],
        table_data : [],
        // tableData:[
        //   { id:'0',metrics_Name: 'team turnover rate',current_value: 0, new_value: 0, },
        //   { id:'1',metrics_Name: 'customer satisfaction',current_value: 0, new_value: 0, },
        //   { id:'2',metrics_Name: 'team size',current_value: 0, new_value: 0, },
        //   { id:'3',metrics_Name: 'budget',current_value: 0,  new_value: 0,},
        //   { id:'4',metrics_Name: 'morale',current_value: 0,value: 0, new_value: 0, },
        //   { id:'5',metrics_Name: 'time allocated',current_value: 0 ,value: 0, new_value: 0, },
        //   { id:'6',metrics_Name: 'code quality',current_value: 0 ,value: 0, new_value: 0,},
        //   { id:'7',metrics_Name: 'code review',current_value: 1,value: 0, new_value: 0, },
        //   { id:'8',metrics_Name: 'deployment',current_value: 1 ,value: 0, new_value: 0,},
        //   { id:'9',metrics_Name: 'lead time',current_value: 1,value: 0, new_value: 0, },
        //   { id:'10',metrics_Name: 'mean time between',current_value: 1,value: 0, new_value: 0,},
        //   { id:'11',metrics_Name: 'codebase size',current_value: 1 ,value: 0, new_value: 0, },
        //   { id:'12',metrics_Name: 'codebase',current_value: 1,value: 0, new_value: 0,  },
        //   { id:'13',metrics_Name: 'mean time to recover',current_value: 1,value: 0, new_value: 0, }
        // ],
        update:false,
      }
    }, 
    watch:{
      project_data(){
        this.table_data = this.project_data.recent_evaluation.improvement_metrics;
      }
    },
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