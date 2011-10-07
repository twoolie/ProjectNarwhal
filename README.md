
ATTENTION
==============

This is a proof of concept implementation of the `ProjectNarwhal` Specification.
It is not to be considered either finished or a definite design direction.
This was my own little proof of concept mockup for fun. (Not trying to muscle in)

Prerequisites
-------------

 * `Compass` framework
 * `SCSS`
 * a `mod_wsgi` capable server (to deploy to)
 
 

Specification
-------------

* Rigorous user authentication
   * plain log-in screen - **IMPLEMENTED**
   * bring back the space invaders game?
   * reset lost passwords
* User designations 
    * administrators (administrate the installation, have direct access to the DB)
    * moderators (can add and remove content through the interface provided)
    * everyone else
    * groups can be created, modified, and given permissions as needed
    * these are **not** user *classes*
* User profile and settings
    * user name
    * verified e-mail
    * password change
    * private key, reset private key
    * set IRC pass
    * avatar
    * clear ledger of all credits (upload and download and other bonuses and expenditures)
* Upload form
    * should be customized with plugins based on content type
    * links to general upload rules and specific rules based on content type
    * very specific data fields for each category
    * helper tools built in if possible (integrated c#bits)
    * torrent parser: can extract metadata if possible (ex container info) and verify file/folder organization follows rules
    * review board submission/needs attention flag (recommended for first time submitters)
* Database
    * attempt backwards compatibility for easy migration
    * stick with MySQL (might be dictated by tracker software depending on what we choose)
* Search
    * solr?
    * should be simple with a complete advanced mode
* Webpage generator from template
    * base template
    * templates for most categories listed here
    * need designs/skins/stylesheets
    * i18n and l10n
* File storage and access
    * handled via DB for the most part
    * content categories handled via plugin
    * stored and displayed with meaningful metadata in an organized way
    * allow user to download .torrent files!
* Torrent page
    * comments
    * mediainfo
    * report function form with prelisted reasons, severity level(?)
    * comments
    * file list
    * peer list
    * stats (torrent size, seeders, leechers, snatches)
    * thanks button
* Tracker
    * roll our own, use the old one (xbtt), or migrate to [another](https://secure.wikimedia.org/wikipedia/en/wiki/Comparison_of_BitTorrent_tracker_software) [one](https://code.google.com/p/django-torrent-tracker/)?
* Request system
    * requests
    * comments
    * bounty, votes
    * link to filling torrent
* Statistics collection, storage and presentation 
    * top 10, 100, 250
    * user stats
    * user classes
    * torrent stats
    * tracker stats
* User to user messaging system
    * inbox
    * sentbox
    * compose
    * delete
    * read/unread distinction, auto mark messages as read, ability to remark them as unread
* Bookmarking system
* RSS Feed generation 
    * needs private key authentication
    * all torrents
    * one for each category
    * user feeds
    * auto-download feed
    * search based feeds
* Forums
    * SPAM FORUM
    * tree-style storage for a reddit-like display (optional)
* Wiki
    * discuss expanding editing permissions
* Bug tracker/support center
    * tickets opened by users
    * status
    * severity
    * comments
* Web-based IRC client