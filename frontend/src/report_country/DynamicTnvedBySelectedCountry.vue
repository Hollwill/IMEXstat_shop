<template>
  <div class="dynamic-selected-tnved">
    <h1>Вовлеченность стран в выбранные кода ТНВЭД</h1>
    <highcharts class="chart" :options="chartOptions" :deepCopyOnUpdate="true" :updateArgs="updateArgs"></highcharts>
    <h1>Динамика выбранных кодов ТНВЭД</h1>
    <div class="d-table">
      <div class="d-tr" v-for="(item, index) in dynamicTable" :key="index">
          <div class="d-td div-as-button" @click="countryDataRequest(item.label)">{{item.label}}</div>
          <div class="d-td">{{item.weight}}</div>
          <div class="d-td">{{item.dynamicWeight}}</div>
          <div class="d-td">{{item.stoim}}</div>
          <div class="d-td">{{item.dynamicStoim}}</div>
      </div>
    </div>
    <h1>Сегментный бублик</h1>
    <highcharts class="chart" :options="firstTnvedCountriesPieOptions" :updateArgs="updateArgs"></highcharts>
    <highcharts class="chart" :options="selectedItemPieOptions" :updateArgs="updateArgs"></highcharts>

    <highcharts class="chart" :options="avgBarOptions"></highcharts>

<!--    <h1>Доля первого кода в вышестоящем</h1>-->
<!--    <highcharts class="chart" :options="firstTnvedPartsPieOptions" :updateArgs="updateArgs"></highcharts>-->
  </div>
</template>

<script>
    import Vue from "vue";
    import HighchartsVue from "highcharts-vue";
    import Highcharts from "highcharts/highcharts";
    import dataModule from "highcharts/modules/data";
    import drilldown from "highcharts/modules/drilldown";
    import {HTTP} from '../http-common'
    import qs from 'qs'
    import moment from 'moment'

    import threeDimensionsHC from "highcharts/highcharts-3d";
    dataModule(Highcharts);
    drilldown(Highcharts);
    threeDimensionsHC(Highcharts);
    Vue.use(HighchartsVue);

    export default {
        name: "DynamicTnvedBySelectedCountry",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        data () {
            return {
                country_data: [],
                date_labels: [],
                updateArgs: [true, true, true],
                avgBarOptions: {
                  chart: {
                      type: 'column'
                  },
                  xAxis: {
                      type: 'category',
                      labels: {
                          rotation: -45,
                          style: {
                              fontSize: '13px',
                              fontFamily: 'Verdana, sans-serif'
                          }
                      }
                  },
                  legend: {
                      enabled: false
                  },
                  series: [{
                      data: [],
                  }]

                },
                chartOptions: {
                  xAxis: {
                      categories: null
                  },
                  series: [
                      {
                          name: 'Импорт',
                          data: []
                      },
                      {
                          name: 'Экспорт',
                          data: []
                      },

                  ]
                },
                selectedItemPieOptions: {
                  plotOptions: {
                    series: {
                      dataLabels: {
                        enabled: true,
                        format: '{point.name}: {point.percentage:.2f}%'
                      }
                    }
                  },
                  tooltip: {
                    // headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                    pointFormat: 'значение: <b>{point.y}</b><br/>'
                  },
                  chart: {
                    type: "pie"
                  },

                  series: [{
                    data: [],
                  }],
                },
                firstTnvedCountriesPieData: [],
                firstTnvedCountriesPieOptions: {
                  plotOptions: {
                    series: {
                      dataLabels: {
                        enabled: true,
                        format: '{point.name}: {point.percentage:.2f}%'
                      }
                    }
                  },
                  tooltip: {
                    // headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                    pointFormat: 'значение: <b>{point.y}</b><br/>'
                  },
                  chart: {
                    type: "pie"
                  },

                  series: [{
                    data: [],
                  }],
                },
            }
        },
        computed: {
            dynamicTable: function() {
                let value = [];
                let weight_arr = [];
                let stoim_arr = [];

                for (let data of this.country_data) {
                    let item = (this.category === 'ИМ') ? data.imp : data.exp
                    let weight = item.weight
                    let stoim = item.cost

                    weight_arr.push(weight)
                    stoim_arr.push(stoim)

                    value.push(
                        {
                            short_label: data.item_short,
                            label: data.item,
                            weight: weight,
                            stoim: stoim,
                        });
                }
                weight_arr = this.dynamics_array(weight_arr);
                stoim_arr = this.dynamics_array(stoim_arr);
                for (let i = 0; i < value.length; i++) {
                    value[i].dynamicWeight = weight_arr[i];
                    value[i].dynamicStoim = stoim_arr[i];
                }
                return value
            },
        },
        watch: {
            firstTnvedCountriesPieData: {
                handler(val) {
                    let sorted_arr = val.slice().sort((a, b) => {
                        if (this.category === 'ИМ') {
                              a = (this.params === 'stoim') ? a.imp.cost : a.imp.weight;
                              b = (this.params === 'stoim') ? b.imp.cost : b.imp.weight;
                          } else {
                              a = (this.params === 'stoim') ? a.exp.cost : a.exp.weight;
                              b = (this.params === 'stoim') ? b.exp.cost : b.exp.weight;
                          }
                        return b - a
                    });
                    let value = []
                    for (let i of sorted_arr.slice(0, 9)) {
                        let data
                        if (this.category === 'ИМ') {
                              data = (this.params === 'stoim') ? i.imp.cost : i.imp.weight
                          } else {
                              data = (this.params === 'netto') ? i.exp.cost : i.exp.weight
                          }
                        value.push({name: i.item, y: data});
                    }
                    let sum_data = 0
                    for (let i of sorted_arr.slice(10)) {
                        let data
                        if (this.category === 'ИМ') {
                              data = (this.params === 'stoim') ? i.imp.cost : i.imp.weight
                          } else {
                              data = (this.params === 'netto') ? i.exp.cost : i.exp.weight
                          }
                        sum_data += data
                    }
                    value.push({name: 'Остальные', y: sum_data})
                    this.firstTnvedCountriesPieOptions.series[0].data = value
                },
                deep: true
            }
        },
        methods: {
            updateselectedItemPie(val) {
              this.selectedItemPieOptions.series[0].data = [];
              for (let el of val) {
                let data;
                if (this.category === 'ИМ') {
                    data = (this.params === 'stoim') ? el.imp.cost : el.imp.weight
                } else {
                    data = (this.params === 'netto') ? el.exp.cost : el.exp.weight
                }
                window.console.log(data, el.item)
                this.selectedItemPieOptions.series[0].data.push([el.item, data])
              }
            },
            updateAvgChart(val) {
              this.avgBarOptions.series[0].data = [];
              for (let i = 0; i < this.date_labels.length; i++) {
                  let data;
                  if (this.category === 'ИМ') {
                      data = (this.params === 'stoim') ? val.imp.cost[i] : val.imp.weight[i]
                  } else {
                      data = (this.params === 'netto') ? val.exp.cost[i] : val.exp.weight[i]
                  }
                  this.avgBarOptions.series[0].data.push([this.date_labels[i], data])
              }
            },
            dynamics_array(arr) {
                let new_arr = [0];
                for (let i = 0; i < arr.length; i++) {
                    let val = (arr[i] === 0) ? 0 : ((arr[i+1] - arr[i])/arr[i] * 100).toFixed(2);
                    new_arr.push(val)
                }
                return new_arr
            },
            recount() {
                HTTP.get('statistic/country_report/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(3, 'year').format('YYYY-MM'),
                        'interval': this.interval,
                        'item_list': this.tnved_list,
                        'item_list_length': this.tnved_list.length,
                        'get': 'country'
                    },
                    paramsSerializer: params => {
                      return qs.stringify(params)
                    }
                })
                    .then(response => {
                        this.firstTnvedCountriesPieData = response.data.pie;
                        this.country_data = response.data.table;
                    })
            },
            countryDataRequest(tnved) {
                HTTP.get('statistic/detailed_country_report/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(3, 'year').format('YYYY-MM'),
                        'interval': this.interval,
                        'item_list': this.tnved_list,
                        'item_list_length': this.tnved_list.length,
                        'item': tnved,
                        'get': 'country'
                    },
                    paramsSerializer: params => {
                      return qs.stringify(params)
                    }
                })
                    .then(response => {
                        this.chartOptions.series[0].data = (this.params === 'stoim') ? response.data.data.imp.cost : response.data.data.imp.weight;
                        this.chartOptions.series[1].data = (this.params === 'stoim') ? response.data.data.exp.cost : response.data.data.exp.weight;
                        this.chartOptions.xAxis.categories = response.data.labels;
                        this.date_labels = response.data.labels;
                        this.updateAvgChart(response.data.data);
                        this.updateselectedItemPie(response.data.extend_data)

                    })
            }
        },
        created() {
            this.$eventHub.$on('recount', this.recount)
        },
        beforeDestroy(){
            this.$eventHub.$off('recount');
        },
    }
</script>

<style scoped>

</style>

