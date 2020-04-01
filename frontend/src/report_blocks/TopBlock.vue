<template>
    <div class="dynamic-selected-tnved">
        <h1>{{headers[0]}}</h1>
        <highcharts class="chart" :options="topChartOptions" :deepCopyOnUpdate="true"></highcharts>
        <h1>{{headers[1]}}</h1>
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
        <h5>{{headers[2]}}</h5>
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

        <h5>{{headers[3]}}</h5>
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
        <h1>{{headers[3]}}</h1>
        <highcharts class="chart" :options="firstPieOptions"></highcharts>
        <h1>{{headers[4]}}</h1>
        <highcharts class="chart" :options="selectSecondPieOptions"></highcharts>
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
        name: "TopBlock",
        props: ['get_by', 'headers', 'date', 'params', 'interval', 'category', 'item_list'],
        data() {
            return {
                tnved_extend_data: [],
                items_data: [],
                date_labels: [],
                topChartOptions: {
                    xAxis: {
                        categories: null
                    },
                    series: []
                },
                imp_sum_table: {
                    stoim: null,
                    weight: null
                },
                exp_sum_table: {
                    stoim: null,
                    weight: null
                },
                firstPieOptions: {
                  plotOptions: {
                    series: {
                      dataLabels: {
                        enabled: true,
                        format: '{point.name}: {point.percentage:.2f}%'
                      }
                    }
                  },
                  tooltip: {
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
                secondCountryPieOptions: {
                    plotOptions: {
                        series: {
                            dataLabels: {
                                enabled: true,
                                format: '{point.name}: {point.percentage:.2f}%'
                            }
                        }
                    },
                    tooltip: {
                        pointFormat: 'value: <b>{point.y}</b><br/>'
                    },
                    chart: {
                        type: "pie"
                    },
                    series: [{
                        data: [],
                    }],
                    drilldown: {
                        series: []
                    }
                },
                secondTnvedPieOptions: {
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
            items_data: {
                handler(val) {
                    this.updateTopChart(val);
                    this.updateSumTables(val);
                    this.updateFirstPie(val);
                    this.updateSecondTnvedPie(this.tnved_extend_data);
                    this.updateSecondCountryPie(val);
                    this.updateAvgChart(val);
                },
                deep: true,
            }
        },
        computed: {
            // eslint-disable-next-line vue/return-in-computed-property
            selectSecondPieOptions: function () {
                if (this.get_by === 'tnved') {
                    return this.secondTnvedPieOptions
                } else if (this.get_by === 'country') {
                    return this.secondCountryPieOptions
                }
            },
            dynamicTable: function () {
                let value = [];
                let i = 0;
                let weight_arr = [];
                let stoim_arr = [];
                for (let date of this.date_labels) {
                    let stoim = 0;
                    let weight = 0;
                    for (let data of this.items_data) {
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
            selectItem(item_data) {
                let data;
                if (this.category === 'ИМ') {
                    data = (this.params === 'stoim') ? item_data.imp.stoim : item_data.imp.weight
                } else {
                    data = (this.params === 'netto') ? item_data.exp.stoim : item_data.exp.weight
                }
                return data
            },
            updateTopChart(val) {
                this.topChartOptions.series = [];
                  for (let item_data of val) {
                      let data;
                      data = this.selectItem(item_data)
                      this.topChartOptions.series.push({name: item_data.item, data: data})
                  }
                  this.topChartOptions.xAxis.categories = this.date_labels
            },
            updateSumTables(val) {
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
            updateFirstPie(val) {
                this.firstPieOptions.series[0].data = [
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
                this.firstPieOptions.drilldown.series[0].data = [];
                this.firstPieOptions.drilldown.series[1].data = [];

                for (let i = 0; i < val.length; i++) {
                    let imp_data = (this.params === 'stoim') ? val[i].imp.stoim : val[i].imp.weight
                    let exp_data = (this.params === 'stoim') ? val[i].exp.stoim : val[i].exp.weight
                    this.firstPieOptions.drilldown.series[0].data.push([val[i].item, imp_data.reduce((a, b) => a + b, 0)])
                    this.firstPieOptions.drilldown.series[1].data.push([val[i].item, exp_data.reduce((a, b) => a + b, 0)])
                }
            },
            updateSecondCountryPie(val) {
                if (this.get_by === 'country') {
                    this.secondCountryPieOptions.drilldown.series = [];
                    for (let i of val) {
                        let data;
                        if (this.category === 'ИМ') {
                            data = (this.params === 'stoim') ? i.imp.stoim : i.imp.weight
                        } else {
                            data = (this.params === 'netto') ? i.exp.stoim : i.exp.weight
                        }
                        let el_index = this.secondCountryPieOptions.drilldown.series.map((el) => el.id).indexOf(val.continent)
                        if (el_index !== -1) {
                            this.secondCountryPieOptions.drilldown.series[el_index].data.push([i.item, data.reduce((a, b) => a + b, 0)])
                        } else {
                            this.secondCountryPieOptions.drilldown.series.push({
                                name: i.continent,
                                id: i.continent,
                                data: [[i.item, data.reduce((a, b) => a + b, 0)]]
                            })
                        }
                    }
                    for (let i of this.secondCountryPieOptions.drilldown.series) {
                        this.secondCountryPieOptions.series[0].data.push({
                            name: i.id, drilldown: i.id, y: i.data.map(item => item[1]).reduce((a, b) => a + b, 0)
                        })
                    }
                }
            },
            updateSecondTnvedPie(val) {
                if (this.get_by === 'tnved') {
                    this.secondTnvedPieOptions.series[0].data = [];
                    for (let i of val) {
                        let data;

                        if (this.category === 'ИМ') {
                            data = (this.params === 'stoim') ? i.imp.stoim : i.imp.weight
                        } else {
                            data = (this.params === 'netto') ? i.exp.stoim : i.exp.weight
                        }
                        this.secondTnvedPieOptions.series[0].data.push({
                            name: i.item,
                            y: data
                        })
                    }
                }

            },
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
            recount() {
                HTTP.get('statistic/report/top_block/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(3, 'year').format('YYYY-MM'),
                        'interval': this.interval,
                        'params': this.params,
                        'category': this.category,
                        'item_list': this.item_list,
                        'item_list_length': this.item_list.length,
                        'get_by': this.get_by,
                    },
                    paramsSerializer: params => {
                        return qs.stringify(params)
                    }
                })
                    .then(response => {
                        this.date_labels = response.data.labels;
                        this.items_data = response.data.data;
                        this.tnved_extend_data = response.data.tnved_extend_data;
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