<template>
  <div class="country-statistic">
    <h1>Вовлечениние стран в ВЭД России</h1>
    <button v-if="table_data.labels[1]" @click="hide_table">Спрятать/показать таблицу</button>
    <div class="d-table" v-if="show_table">
      <div class="d-tr" v-for="(label, index) in table_data.labels" :key="index">
        <div class="d-td div-as-button" @click="extendTnved(label)">{{label}}</div>
        <div class="d-td">{{table_data.netto[0][index]}}</div>
        <div class="d-td">{{table_data.netto[1][index]}}</div>
        <div class="d-td">{{table_data.cost[0][index]}}</div>
        <div class="d-td">{{table_data.cost[1][index]}}</div>
      </div>
    </div>
  </div>
</template>

<script>
    import {HTTP} from '../http-common'
    import moment from 'moment'

    export default {
        name: "CountryStatistic",
        props: ['date', 'interval', 'params', 'category',],
        data() {
            return {
              table_data: {
                  labels: [],
                  netto: [[], []],
                  cost: [[], []],
              },
              show_table: true
            }
        },
        methods: {
            recount() {
                HTTP.get('statistic/country_statistic/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(1, 'year').format('YYYY-MM'),
                        'category': this.category
                    }
                })
                    .then(response => {
                        this.table_data.labels = response.data.table.labels

                        this.table_data.netto[0] = response.data.table.netto[0]
                        this.table_data.netto[1] = response.data.table.netto[1]
                        this.table_data.cost[0] = response.data.table.cost[0]
                        this.table_data.cost[1] = response.data.table.cost[1]
                    })
                    .catch(error => {
                        window.console.log(error)
                    })
            },
            hide_table() {
                this.show_table = (!this.show_table)
            }
        },
        mounted() {
            this.recount()
        },
    }
</script>

<style scoped>
*{
  box-sizing: border-box;
}
.d-table{
  display: table;
  width: 100%;
  border-collapse: collapse;
}
.d-tr{
  display: table-row;
}
.d-td{
  display: table-cell;
  text-align: center;
  border: none;
  border: 1px solid #ccc;
  vertical-align: middle;
}
.d-td:not(.no-p){
  padding: 4px;
}
.div-as-button {
  cursor: pointer;
}
</style>