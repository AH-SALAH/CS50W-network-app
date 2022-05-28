<h1 align="center">Network</h1>

<p align="center">
  <img align="center" alt="Github top language" src="https://img.shields.io/github/languages/top/AH-SALAH/
CS50W-network-app?color=56BEB8" />
  <img align="center" alt="Github language count" src="https://img.shields.io/github/languages/count/AH-SALAH/CS50W-network-app?color=56BEB8" />
  <img align="center" alt="Repository size" src="https://img.shields.io/github/repo-size/AH-SALAH/
CS50W-network-app?color=56BEB8" />
  <img align="center" alt="License" src="https://img.shields.io/github/license/AH-SALAH/
CS50W-network-app?color=56BEB8" />
  <img align="center" alt="Github issues" src="https://img.shields.io/github/issues/AH-SALAH/
CS50W-network-app?color=56BEB8" />
  <img align="center" alt="Github forks" src="https://img.shields.io/github/forks/AH-SALAH/
CS50W-network-app?color=56BEB8" />
  <img align="center" alt="Github stars" src="https://img.shields.io/github/stars/AH-SALAH/
CS50W-network-app?color=56BEB8" />
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Network 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/AH-SALAH" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

CS50W Proj4 Network App - Twitter Like [App](https://cs50-network-twitter.herokuapp.com/) - [YT video](https://youtu.be/huFoZvwe388)

## :sparkles: Features ##

:heavy_check_mark: All Posts\
:heavy_check_mark: Add Post\
:heavy_check_mark: Edit Post\
:heavy_check_mark: Profile\
:heavy_check_mark: Followings\
:heavy_check_mark: Follow/Unfollow\
:heavy_check_mark: Like/Unlike\
:heavy_check_mark: Pagination

## :rocket: Technologies ##

The following tools were used in this project:

- Django
- React
- Jsx
- ReactQuery
- ES6

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com), [Node](https://nodejs.org/en/), [Python](https://python.org) and [Docker](https://docker.com) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone this repo

# Access
$ cd network
$ fill the data in env/*.env files [secrets, db, db_name, host, password, etc..]
$ change .env files from *-sample to same without '-sample' suffix
# $ ex: db_admin_dev-sample.env => db_admin_dev.env

# Install dependencies
# - install docker images
    # for dev
    $ docker compose up build
    # for prod
    $ docker compose docker-compose.prod.yml up build
    # ** command with `build` for the first time to download images, afterwards without.


# Run the project
$ open <http://localhost> in browser for django app

# for custom domain to work
# you need to modify & set them in etc/host file as 
# 127.0.0.1 backend.com
# 127.0.0.1 dbadmin.com //for postgres db-admin browser version
# $ then open "http://backend.com" in browser for django app
# $ & open "http://dbadmin.com" in browser for dbadmin

```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :duck: by <a href="https://github.com/AH-SALAH" target="_blank">AH-SALAH</a>

&#xa0;

<a href="#top">Back to top</a>
