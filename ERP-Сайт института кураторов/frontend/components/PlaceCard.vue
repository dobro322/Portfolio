<template>
  <v-content>
    <v-dialog
       v-if="chosen_date"
      v-model="reserv_dial.visible"
      max-width="500px"
    >
      <v-card class="rounded">
        <div v-if="!$vuetify.breakpoint.xs">
          <v-img style="height:250px; width:auto" :src="place.photo"></v-img>
        </div>
        <v-card-title primary-title>
          <v-layout row wrap>
            <v-flex xs12>
              <div class="headline">
                <p>{{ place.name }}</p>
              </div>
            </v-flex>
            <v-flex xs12>
              <div class="body">
                <p>{{ place.description }}</p>
              </div>
            </v-flex>
          </v-layout>
        </v-card-title>

        <v-layout class="px-2 pb-4 pt-2" style="border-top:solid; border-color:rgba(0,0,0,.3); border-width:2px" row wrap>
          <v-flex xs12>
            <div class="headline text-xs-center"><p>Выберите время окончания</p></div>
          </v-flex>
          <v-flex xs12 v-for="hour in (0, ( (cut_time_panel.length%4 === 0) ? (cut_time_panel.length / 4) : (parseInt(cut_time_panel.length / 4) + 1)))" >
            <v-layout align-center row wrap>
                <v-flex class="subheading" xs12  v-if="cut_time_panel[(hour - 1) * 4].time >= chsn_time[0] + chsn_time[1] + ':00'">
                  <p>{{ cut_time_panel[(hour - 1) *4].time }}</p>
                </v-flex>
                <v-flex class="px-1" xs3 v-for="minutes in (0, 4)" v-if="cut_time_panel[(hour-1)*4 + minutes - 1]">
                  <v-card v-if="cut_time_panel[(hour-1)*4 + minutes - 1].time >= chsn_time" @click="" :style="(chsn_time === cut_time_panel[(hour-1)*4 + minutes - 1].time ? 'border-style:solid; border-color:purple' : '') " :class="'py-1 rounded text-xs-center' + (cut_time_panel[(hour-1)*4 + minutes - 1].free ? '' : ' noselect grey lighten-2')" :hover="cut_time_panel[(hour-1)*4 + minutes - 1].free ? true : false">
                    <p> {{cut_time_panel[(hour-1)*4 + minutes - 1].time}}</p>
                  </v-card>
                </v-flex>
              </v-layout>
          </v-flex>
          <v-flex pt-4 xs12 text-xs-center>
              <div class="subheading text-xs-center"><p> +15 минут на уборку</p></div>
          </v-flex>
        </v-layout>

      </v-card>
    </v-dialog>
    <v-card class="rounded">
      <div v-if="!$vuetify.breakpoint.xs">
        <v-img style="height:150px; width:auto" :src="place.photo"></v-img>
      </div>
      <v-card-title primary-title>
        <div class="headline">
          <p>{{ place.name }}</p>
        </div>
        <div class="body">
          <p>{{ place.description }}</p>
        </div>
      </v-card-title>
      <v-layout ref="time_panel" v-if="chosen_date" class="px-2 scroll" style="border-top:solid; border-color:rgba(0,0,0,.3); border-width:2px; height:200px" row wrap>

        <v-flex :ref="time_sheet[hour * 4].time" xs12 v-for="hour in [0,1,2,3,4,5,6,7,8,9]">
            <v-layout align-center row wrap>
              <v-flex class="subheading" xs12>
                <p>{{ time_sheet[hour *4].time }}</p>
              </v-flex>
              <v-flex class="px-1" xs3 v-for="minutes in [0,1,2,3]">
                <v-card @click="open_dial(time_sheet[hour * 4 + minutes].time)" :style="(chsn_time === time_sheet[hour * 4 + minutes].time ? 'border-style:solid; border-color:purple' : '') " :class="'py-1 rounded text-xs-center' + (time_sheet[hour * 4 + minutes].free ? '' : ' noselect grey lighten-2')" :hover="time_sheet[hour * 4 + minutes].free ? true : false">
                  <p> {{time_sheet[hour * 4 + minutes].time}}</p>
                </v-card>
              </v-flex>
            </v-layout>
        </v-flex>
      </v-layout>


    </v-card>
  </v-content>
</template>
<script>
import axios from 'axios'
import format from 'date-fns/format'
import VueOverflowScroll from 'vue-overflow-scroll'

  export default {
    directives: {
    	'v-overflow-scroll': VueOverflowScroll
    },
    props: ["place","chosen_date","chosen_time"],
    methods: {
      generate_time_panel(){
        var timeArr = new Array()
        var date = new Date(this.chosen_date*1000 + 36000*1000)
        for (var i = 1; i <= 40; i++){
          timeArr.push({
            "time": date.getHours() + ":" + ( date.getMinutes() === 0 ? "00" : date.getMinutes()),
            "free": this.place.reservation_time.find(a=>{
              if(a.time_start <= date.getTime()/1000+60*60*3 && a.time_end > date.getTime()/1000+60*60*3) return 1
              else return 0
            }) ? 0 : 1
          })
          date = new Date(date.getTime() + 60*15*1000)
        }
        this.time_sheet = timeArr
      },
      open_dial(time){
        this.chsn_time = time
        this.reserv_dial.visible = true
      },
    },
    computed:{
      cut_time_panel(){
        var b = new Array()
        var counter = 12;
        for(var i = this.chsn_time[1] * 4; i<40 ; i++){
          if(!this.time_sheet[i].free) break;
          if(counter === 0) break;
          b.push(this.time_sheet[i])
          if(this.chsn_time <= this.time_sheet[i].time) counter-=1
        }
        return b
      },
      chsn_time:{
        get(){
          return this.chosen_time
        },
        set(arg){
          this.$emit("change_time", arg)
          return this.chosen_time
        }
      }
    },
    watch:{
      chosen_date: function(){
        this.generate_time_panel()
      },
      chosen_time: function(){
        var offset = this.$refs[this.chosen_time[0] + this.chosen_time[1] + ":00"][0].offsetTop - this.$refs["10:00"][0].offsetTop
        this.$refs.time_panel.scrollTo(0, offset);
      }
    },
    data(){
      return{
        time_sheet: [],
        reserv_dial: {
          visible: false,
          show_time: true
        }
      }
    },
    created(){}
}
</script>

<style>

</style>
