import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { Http } from '@angular/http';

import { BarcodeScanner, BarcodeScannerOptions, BarcodeScanResult } from '@ionic-native/barcode-scanner';
import { BrowserTab } from '@ionic-native/browser-tab';

let imagePaths = {
  'ap'     : 'assets/imgs/ap.svg',
  'Wireless Controller'   : 'assets/imgs/wlan-ctrl.svg',
  'switch' : 'assets/imgs/switch.svg',
  'unknown': 'assets/imgs/unknown.svg'
}


//const INFO_URL = 'http://173.39.52.48:7001/info';
//const HEALTH_URL = 'http://173.39.52.48:7001/health';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  private result        : BarcodeScanResult;
  private macAddr       : string;

  private deviceInfo    : any;
  private deviceHealth  : any;

  private isScanned     : boolean;
  private isKnownDevice : boolean;
  private imagePath     : string;
  private dnacIp        : string;

  private scanEnabled   : boolean;
  private isShowMore    : boolean;

  constructor(private navCtrl: NavController, private barcode: BarcodeScanner, private browser: BrowserTab, private http: Http) {
  }

  ionViewDidLoad(){
    this.isScanned     = false;
    this.isKnownDevice = false;
    this.imagePath     = imagePaths.unknown;
    this.macAddr       = '';

    this.deviceInfo   = {};
    this.deviceHealth = {};

    this.scanEnabled  = false;
    this.isShowMore = false;
    //this.mock();
  }

  getUrl(urlSuffix: string): string{
    return `http://${this.dnacIp}:7001/${urlSuffix}`;
  }

  showMore() {
    this.isShowMore = true;
  }

  updateIp(){
    this.scanEnabled = true;
    //no action necessary as we are using 2-way data-binding
    console.log("Updated IP to:", this.dnacIp);
  }

  getDeviceInfo(macAddr: string){
    let url = this.getUrl('info_dnac');
    this.http.get(`${url}/${macAddr}`).subscribe(
      (response) => {
        this.deviceInfo = response.json();
        console.log("> Device Info:", this.deviceInfo);
        this.isKnownDevice = (this.deviceInfo._id != undefined) ? true : false;
        this.imagePath = imagePaths[this.deviceInfo.type];
      },
      (error) => {
        console.error(error);
      }
    );
  }


  getData(macAddr: string){
    this.getDeviceInfo(macAddr);
    //this.getDeviceHealth(macAddr);
  }

  mock(){
    this.macAddr = 'E865.4921.17A5'; //ap
    this.macAddr = '00:57:D2:B4:FF:80'; //switch
    this.macAddr = '70:DB:98:BC:E7:80'; //ctrl

    this.isScanned = true;
    this.getData(this.macAddr);
  }

  doScan(){
    const options: BarcodeScannerOptions = {
      showTorchButton: true,
      resultDisplayDuration: 3000,
      prompt: 'Scan QR code on the device',
    }

    this.barcode.scan(options).then(
      (response) => {
        this.result    = response;
        this.isScanned = true;

        console.log("Scanned result:", this.result);
        this.macAddr = this.result.text;
        this.getData(this.macAddr);
      },
      (error) => {
        console.error(error);
    });
  }
}
