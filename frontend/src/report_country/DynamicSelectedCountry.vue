<template>
  <div class="dynamic-selected-tnved">
    <h1>Динамика выбранных стран</h1>
    <highcharts class="chart" :options="chartOptions" :deepCopyOnUpdate="true" :updateArgs="updateArgs"></highcharts>
    <h1>Динамика выбранных стран</h1>
    <div class="d-table">
      <div class="d-tr" v-for="(item, index) in dynamicTable" :key="index">
          <div class="d-td">{{item.label}}</div>
          <div class="d-td">{{item.weight}}</div>
          <div class="d-td">{{item.dynamicWeight}}</div>
          <div class="d-td">{{item.stoim}}</div>
          <div class="d-td">{{item.dynamicStoim}}</div>
      </div>
    </div>
    <br>
    <h5>суммарный импорт по выбранным странам</h5>
    <div class="d-table" style="width: 50% !important;">
      <div class="d-tr">
        <div class="d-td">{{imp_sum_table.stoim}}</div>
        <div class="d-td">$</div>
      </div>
      <div class="d-tr">
        <div class="d-td">{{imp_sum_table.weight}}</div>
        <div class="d-td">т</div>
      </div>
    </div>
    <h5>суммарный экспорт по выбранным странам</h5>
    <div class="d-table" style="width: 50% !important;">
      <div class="d-tr">
        <div class="d-td">{{exp_sum_table.stoim}}</div>
        <div class="d-td">$</div>
      </div>
      <div class="d-tr">
        <div class="d-td">{{exp_sum_table.weight}}</div>
        <div class="d-td">т</div>
      </div>
    </div>
    <h1>Сегментный бублик</h1>
    <highcharts class="chart" :options="segmentPieOptions" :updateArgs="updateArgs"></highcharts>
    <highcharts class="chart" :options="avgBarOptions"></highcharts>

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
        name: "DynamicSelectedCountry",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        data () {
            return {
                tnved_extend_data: [],
                tnved_data: [],
                date_labels: [],
                imp_sum_table: {
                    stoim: null,
                    weight: null
                },
                exp_sum_table: {
                    stoim: null,
                    weight: null
                },
                updateArgs: [true, true, true],
                segmentPieOptions: {
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
                    pointFormat: 'value: <b>{point.y}</b><br/>'
                  },
                  chart: {
                    type: "pie"
                  },

                  series: [{
                    data: [],
                  }],
                  drilldown:{
                    series:[
                        {
                            name: 'Импорт',
                            id: 'imp',
                            data: [],
                        },
                        {
                            name: 'Экспорт',
                            id: 'exp',
                            data: [],
                        }
                    ]
                  }
                },
                chartOptions: {
                  xAxis: {
                      categories: null
                  },
                  title: {
                    text: 'Sin chart'
                  },
                  series: []
                },
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

                  }
            }
        },
        watch: {
            tnved_data: {
                handler(val) {
                    this.updateAvgChart(val);
                    this.updateLineChart(val);
                    this.sumTables(val);
                    this.segmentPieData(val);
                },
                deep: true
            }
        },
        computed: {
            dynamicTable: function() {
                let value = [];
                let i = 0;
                let weight_arr = [];
                let stoim_arr = [];
                for (let date of this.date_labels) {
                    let stoim = 0;
                    let weight = 0;
                    for (let data of this.tnved_data) {
                        let item = (this.category === 'ИМ') ? data.imp : data.exp
                        weight += item.weight[i]
                        stoim += item.stoim[i]

                    }
                    weight_arr.push(weight)
                    stoim_arr.push(stoim)
                    value.push(
                        {
                            label: date,
                            weight: weight,
                            stoim: stoim,
                        });
                    i++
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
        methods: {
            updateAvgChart(val) {
              this.avgBarOptions.series[0].data = [];
              for (let i = 0; i < this.date_labels.length; i++) {
                let sum = 0;
                for (let el of val) {
                  let data;
                  if (this.category === 'ИМ') {
                      data = (this.params === 'stoim') ? el.imp.stoim[i] : el.imp.weight[i]
                  } else {
                      data = (this.params === 'netto') ? el.exp.stoim[i] : el.exp.weight[i]
                  }
                  sum += data
                }
                this.avgBarOptions.series[0].data.push([this.date_labels[i], sum / val.length])
              }
            },
            segmentPieData(val) {
                this.segmentPieOptions.series[0].data = [
                    {
                        name: 'Импорт',
                        y: (this.params === 'stoim') ? this.imp_sum_table.stoim : this.imp_sum_table.weight,
                        drilldown: 'imp',
                        color: '#0600FF'
                    },
                    {
                        name: 'Экспорт',
                        y: (this.params === 'stoim') ? this.exp_sum_table.stoim : this.exp_sum_table.weight,
                        drilldown: 'exp',
                        color: '#EBFF00'
                    }
                ];
                this.segmentPieOptions.drilldown.series[0].data = [];
                this.segmentPieOptions.drilldown.series[1].data = [];

                for (let i = 0; i < val.length; i++) {
                    let imp_data = (this.params === 'stoim') ? val[i].imp.stoim : val[i].imp.weight
                    let exp_data = (this.params === 'stoim') ? val[i].exp.stoim : val[i].exp.weight
                    this.segmentPieOptions.drilldown.series[0].data.push([val[i].item, imp_data.reduce((a, b) => a + b, 0)])
                    this.segmentPieOptions.drilldown.series[1].data.push([val[i].item, exp_data.reduce((a, b) => a + b, 0)])
                }

            },
            sumTables(val) {
                let imp = {stoim: 0, weight: 0};
                let exp = {stoim: 0, weight: 0};
                for (let item of val) {
                    imp.stoim += item.imp.stoim.reduce((a, b) => a + b, 0);
                    imp.weight += item.imp.weight.reduce((a, b) => a + b, 0);
                    exp.stoim += item.exp.stoim.reduce((a, b) => a + b, 0);
                    exp.weight += item.exp.weight.reduce((a, b) => a + b, 0);
                }
                this.imp_sum_table = imp;
                this.exp_sum_table = exp;
            },
            dynamics_array(arr) {
                let new_arr = [0];
                for (let i = 0; i < arr.length; i++) {
                    let val = (arr[i] === 0) ? 0 : ((arr[i+1] - arr[i])/arr[i] * 100).toFixed(2);
                    new_arr.push(val)
                }
                return new_arr
            },
            updateLineChart(val) {
                this.chartOptions.series = [];
                  for (let tnved_data of val) {
                      let data;
                      if (this.category === 'ИМ') {
                          data = (this.params === 'stoim') ? tnved_data.imp.stoim : tnved_data.imp.weight
                      } else {
                          data = (this.params === 'netto') ? tnved_data.exp.stoim : tnved_data.exp.weight
                      }
                      this.chartOptions.series.push({name: tnved_data.item, data: data})
                  }
                  this.chartOptions.xAxis.categories = this.date_labels
            },
            recount() {
                HTTP.get('statistic/tnved_dynamics/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(3, 'year').format('YYYY-MM'),
                        'interval': this.interval,
                        'params': this.params,
                        'category': this.category,
                        'item_list': this.tnved_list,
                        'item_list_length': this.tnved_list.length,
                        'get': 'country'
                    },
                    paramsSerializer: params => {
                      return qs.stringify(params)
                    }
                })
                    .then(response => {
                        this.date_labels = response.data.labels
                        this.tnved_data = response.data.data
                        this.tnved_extend_data = response.data.tnved_extend_data
                    })
                    .catch(error => {
                        window.console.log(error)
                    })
            },
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

