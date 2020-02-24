<template>
  <v-layout justify-center>
    <v-dialog
      scrollable
      v-model="show"
      persistent
      max-width="500px"
    >
    <v-card>
      <v-card-title class="display-1"><p>{{ abit.full_name }}</p></v-card-title>
      <v-card-text>
        <v-layout row wrap>
          <v-flex xs12 v-for="predict in abit.predictings.filter(a=>{return a.failed === false})">
            <v-card class="pa-4">
              <v-layout align-center row wrap>
                <v-flex xs12>
                  <v-layout row wrap>

                  </v-layout>
                  <v-layout align-center text-xs-center text-sm-left row wrap>
                    <v-flex md4 xs12>
                      <v-avatar
                      size="100px"
                      >
                        <v-img :src="predict.photo_100" alt="alt"></v-img>
                      </v-avatar>
                    </v-flex>
                    <v-flex md8 xs12>
                      <v-layout row wrap>
                        <v-flex class="headline">
                          <p><a style="text-decoration:none" :href="'https://vk.com/id' + predict.id" target="_blank">{{predict.first_name}} {{predict.last_name}}</a></p>
                        </v-flex>
                        <v-flex  class="title" xs12>
                          <p>Др: {{predict.bdate}}</p>
                        </v-flex>
                        <v-flex xs12>
                          <p>Комментарий: {{predict.comment}}</p>
                        </v-flex>
                      </v-layout>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex text-xs-center xs12>
                  <v-btn flat class="elevation-2" @click="success(predict)" block color="green">Подтвердить</v-btn>
                  <v-btn flat class="elevation-2" @click="failed(predict)" block color="red">Исключить</v-btn>
                </v-flex>
              </v-layout>
            </v-card>
          </v-flex>
          <v-flex v-if="abit.predictings.filter(a=>{return a.failed === false}).length === 0"><p>Предложение отсутствует</p></v-flex>
        </v-layout>
      </v-card-text>
      <v-card-actions class="px-4">
        <v-layout justify-space-around row wrap>
          <v-btn color="orange" @click="$emit('close')" flat block><p>Закрыть</p></v-btn>
        </v-layout>
      </v-card-actions>
    </v-card>
    </v-dialog>
    <YNPanel :func="ynpanel.function" @no="ynpanel.visible = false" :visible="ynpanel.visible" :header="ynpanel.header" :text="ynpanel.text"></YNPanel>
  </v-layout>
</template>

<script>
import format from 'date-fns/format'
import YNPanel from '../components/YNPanel.vue'

  export default {
    components:{YNPanel},
    methods:{
      failed(predict){
        predict.name = 'vk.com/id' + predict.id
        this.ynpanel = {
          header: predict,
          visible: true,
          text: 'Подтвердить промах?'
        }
        this.ynpanel.function = (predict => {
          this.$emit('failed', predict)
        })
      },
      success(predict){
        predict.name = 'vk.com/id' + predict.id
        this.ynpanel = {
          header: predict,
          visible: true,
          text: 'Подтвердить попадание?'
        }
        this.ynpanel.function = (predict => {
          this.$emit('success', predict)
        })
      }
    },
    computed:{
      show: {
        get () {
          return this.visible
        },
        set (value) {
          this.$emit('close')
          return value
        },
      },
    },
    created(){
      this.user = this.abit
    },
    props: ['abit', 'visible'],
    data(){
      return{
        ynpanel: {
          visible: false,
          header: '',
          text: '',
          function: a =>{return a}
        },
        user: {
          full_name: '',
          predictings: [
            {
              'vk': 12345,
              'failed': false,
              'comment': 'Др'
            }
          ]
        }
      }
    }
  }
</script>

<style>

</style>
