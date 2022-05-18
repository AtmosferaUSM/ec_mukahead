<!-- Badges -->
![GitHub](https://img.shields.io/github/license/AtmosferaUSM/ec_mukahead?label=license&logo=Github&style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/AtmosferaUSM/ec_mukahead?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/AtmosferaUSM/ec_mukahead?color=yellow&style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/AtmosferaUSM/ec_mukahead?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/AtmosferaUSM/ec_mukahead?logo=Github&style=for-the-badge)
![Custom badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fsn7hcohj4l.execute-api.us-west-2.amazonaws.com%2Fv1%2Fgithub&style=for-the-badge&color=138)




<div id="top"></div>

<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://atmosfera.usm.my/index.html" target="_blank">
    <img src="https://github.com/AtmosferaUSM/ec_mukahead/blob/main/images/white-logo.jpg" alt="Logo">
  </a>

  <h3 align="center">Muka Head Station's Eddy Covariance and Biomet Data</h3>

  <p align="center">
    The eddy covariance and biomet data transfer code that tranfer them from the local server to the cloud for the Muka Head station.
    <br />
    <a href="https://atmosfera.usm.my/index.html" target="_blank"><strong>Explore the Atmosfera research website »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The Atmosfera research website showcases our ongoing research in atmosphere-sea and land interactions. Currently, we study the atmospheric exchanges above sea and freshwater bodies. We hope to measure the fluxes for many years to come so that we gain in-depth insights on the short-term and long-term atmospheric processes of these surfaces. We explore these interactions using theeddy covariance" method, a fast response open-path gas analyzer and anemometer system capable in measuring fluxes of moisture and carbon dioxide. To support the flux data, we measure weather parameters, such as solar radiation, temperature, relative humidity and wind so that we get a better understanding of the feedbacks and responses of the exchanges and its drivers.

The Github repo stores the codes we use in transferring the data on the local server to a cloud database on Amazon Web Services (AWS) servers. The data also can be downloaded using an API on the atmosfera.usm.my website.

`yusriyp`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

List of programming languages and services used for this project.

* [Python 3](https://www.python.org/)
* [AWS S3](https://aws.amazon.com/s3/)
* [AWS DynamoDB](https://aws.amazon.com/dynamodb/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [AWS Cloud9](https://aws.amazon.com/cloud9/)
* [AWS API Gateway](https://aws.amazon.com/api-gateway/)
* [AWS CloudWatch](https://aws.amazon.com/cloudwatch/)
* [AWS Cognito](https://aws.amazon.com/cognito/)
* [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/)
* [Amazon Simple Notification Service](https://aws.amazon.com/sns/)


<!-- GETTING STARTED -->
## Getting Started

give instructions on setting up the project.
simple example steps.

### Prerequisites

list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

<div align="center">
    <img src="https://github.com/AtmosferaUSM/ec_mukahead/blob/main/images/Local_to_S3.jpg" alt="Logo" width="80%" height="80%">
 </div>
 <div align="center">
    <img src="https://github.com/AtmosferaUSM/ec_mukahead/blob/main/images/s3_to_dynamodb_lambda.JPG" alt="Logo" width="80%" height="80%">
 </div>
 <div align="center">
    <img src="https://github.com/AtmosferaUSM/ec_mukahead/blob/main/images/s3_to_dynamodb_cloud9.JPG" alt="Logo" width="80%" height="80%">
 </div>
 <div align="center">
    <img src="https://github.com/AtmosferaUSM/ec_mukahead/blob/main/images/api.JPG" alt="Logo" width="80%" height="80%">
 </div>
 
 

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

how a project can be used, demos and more resources.


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/AtmosferaUSM/ec_mukahead/issues) for a full list of proposed features (and known issues).


<blockquote>
  Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim
</blockquote>

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Creators

#### Dr. Yusri Yusup
<div>
    <a href="https://sites.google.com/site/yusriyp" target="_blank">
        <img src="https://img.shields.io/badge/website-sites.google.com/site/yusriyp-green?style=for-the-badge&logo=appveyor" alt="website">
    </a>
    <a href="nailto:yusriy@usm.my" target="_blank">
        <img src="https://img.shields.io/badge/email-yusriy@usm.my-important?style=for-the-badge" alt="email">
    </a>
    <a href="https://www.linkedin.com/in/yusriy/" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="linkeddin">
    </a>
    <a href="https://www.youtube.com/channel/UCAGpbU_rdH7sTMUZPn9r67w" target="_blank">
        <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="youtube">
    </a>
</div>



#### Ehsan Jolous Jamshidi
<div>
    <a href="https://jamshidi.herokuapp.com/" target="_blank">
        <img src="https://img.shields.io/badge/website-jamshidi.herokuapp.com-green?style=for-the-badge&logo=appveyor" alt="website">
    </a>
    <a href="nailto:ej.jamshidi@gmail.com" target="_blank">
        <img src="https://img.shields.io/badge/email-ej.jamshidi@gmail.com-important?style=for-the-badge" alt="email">
    </a>
    <a href="https://my.linkedin.com/in/ehsan-jolous-jamshidi-19a2b6146" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="linkeddin">
    </a>
</div>


#### Atmosfera Website Social Media
<div>
<a href="https://www.facebook.com/atmosphereInteraction" target="_blank">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="facebook">
</a>

<a href="https://www.linkedin.com/company/atmosphere-interaction" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="linkeddin">
</a> 
</div>

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This research is funded by the `Universiti Sains Malaysia` Research University Grant No. `1001/PTEKIND/811316` and Bridging Grant 2018 Grant No. `304.PTEKIND.6316289`.
      
Some of the sensors used are contributed by `Elite Scientific Instruments` <br />
:office: Sdn Bhd. A-LG-03, Block A, Serdang Perdana Selatan, Section 1, 43300 Seri Kembangan, Selangor Darul Ehsan, Malaysia <br />
:phone: +603 89456100; +603 89454613 (Office) <br />
:fax:  +603 8945 7100 <br />
:email: sales@esi.com.my <br />






<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

