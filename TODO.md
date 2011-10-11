
======
 TODO
======

 * [IN PROGRESS -tw] get solr search running
 * [NEW] Facet Search resuls. <http://docs.haystacksearch.org/dev/faceting.html#what-is-faceting>
 * [NEW] Integrate django-notification <= django-mailer
 * [IN PROGRESS -tw] create core API for annotating onto torrent/profile models
   * profiles already started: avatar framwork & online tracking implemented.
 * [STARTED -tw] XBTT support
   * tables just need flag choices set.
   * Write xbtt importer - use xbtt tables to import into core.tracker tables.
     * django tracker + aggressive caching is FAST. Automatic/immediate indexing
   * abstraction api/backend for using it raw/replacing core.torrent/core.tracker with xbt tables.
     * xbtt tracker is well knowm (not well documented), solr indexing is manual.
 * [STARTED -tw] plugins
   * plugins.irc.torrentbot
     * Ask torrentbot about the tracker state.
     * Search tracker through torrentbot - get back either infohash or DCC torrent
     * [admin] get reports of server events.
   * plugins.user.invite
     * allow sending of invites, who invited who [doubles as verified email address]
   * plugins.user.reputation
     * integrate with djangobb or separate?
   * plugins.video.movies
     * extra filters and schema to manage/validate movie information [imdbid/extradata]
   * plugins.video.tv
     * schema for tv shows: episodes & series
   * plugins.music
     * generic music schema. can be extended for specialist music trackers
 * djangobb integration? may need to override djangobb models on the fly.
   * integrate djangobb reputation into the mix?