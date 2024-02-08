import { makeAutoObservable } from 'mobx'

export default class GeneralStore {

  constructor() {
    this._params = {
      groupBy: '',
      metrics: '',
      granularity: '',
    }
    makeAutoObservable(this)
  }

  get params() {
    return this._params;
  }

  setParams(obj) {
    this._params = obj
  }

}