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
    <p>Импорт<input type="checkbox" name="type"  v-model="showImpMap"></p>
    <p>Экспорт<input type="checkbox" name="type"  v-model="showExpMap"></p>
    <highcharts :constructor-type="'mapChart'" :options="impMapOptions" v-if="showImpMap"></highcharts>
    <highcharts :constructor-type="'mapChart'" :options="expMapOptions" v-if="showExpMap"></highcharts>
  </div>
</template>

<script>
    import {HTTP} from '../http-common'
    import moment from 'moment'


    import Vue from 'vue'
    import HighchartsVue from 'highcharts-vue'
    import Highcharts from 'highcharts'
    import mapInit from 'highcharts/modules/map'
    import addWorldMap from '../js/worldmap'

    mapInit(Highcharts)
    addWorldMap(Highcharts)
    Vue.use(HighchartsVue)

    export default {
        name: "CountryStatistic",
        props: ['date', 'interval', 'params', 'category',],
        data() {
            return {
              showImpMap: true,
              showExpMap: false,
              expMapData: [],
              impMapData: [],
              impMapOptions: {
                chart: {
                  map: 'myMapName'
                },
                title: {
                  text: ''
                },
                subtitle: {
                  text: ''
                },
                mapNavigation: {
                  enabled: true,
                  buttonOptions: {
                    alignTo: 'spacingBox'
                  }
                },
                colorAxis: {
                  minColor: '#add8e6',
                  maxColor: '#0000ff'
                },
                series: [
                {
                  name: 'Импорт',
                  states: {
                    hover: {
                      color: '#BADA55'
                    }
                  },
                  allAreas: true,
                  data: []
                }]
              },
              expMapOptions: {
                chart: {
                  map: 'myMapName'
                },
                title: {
                  text: ''
                },
                subtitle: {
                  text: ''
                },
                mapNavigation: {
                  enabled: true,
                  buttonOptions: {
                    alignTo: 'spacingBox'
                  }
                },
                colorAxis: {
                  minColor: '#ffff00',
                  maxColor: '#ffa500'
                },
                series: [
                {
                  name: 'Импорт',
                  states: {
                    hover: {
                      color: '#BADA55'
                    }
                  },
                  allAreas: true,
                  data: []
                }]
              },
              table_data: {
                  labels: [],
                  netto: [[], []],
                  cost: [[], []],
              },
              show_table: true
            }
        },
        watch: {
            expMapData (newValue) {
                this.impMapOptions.series[0].data = newValue
            },
            impMapData (newValue) {
                this.expMapOptions.series[0].data = newValue
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
                        this.expMapData = response.data.chart.imp
                        this.impMapData = response.data.chart.exp
                    })
                    .catch(error => {
                        window.console.log(error)
                    })
            },
            hide_table() {
                this.show_table = (!this.show_table)
            }
        },
        created() {
            this.$eventHub.$on('recount', this.recount)
        },
        beforeDestroy(){
            this.$eventHub.$off('recount');
        },
        mounted() {
            this.recount()
        },
    }
</script>

<style scoped>

</style>