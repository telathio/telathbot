CREATE DATABASE xenforo;
USE xenforo;
CREATE TABLE xf_post
(
    post_id           int unsigned auto_increment
        primary key,
    thread_id         int unsigned                                               not null,
    username          varchar(50)                                                not null,
    reactions         blob                                                       null,
    reaction_users    blob                                                       not null
);
INSERT INTO xenforo.xf_post (post_id, thread_id, username, reactions, reaction_users) VALUES (1, 2, 'User', 0x7B223130223A322C2232223A317D, 0x5B7B22757365725F6964223A34382C22757365726E616D65223A224C696168616C222C227265616374696F6E5F6964223A31307D2C7B22757365725F6964223A35382C22757365726E616D65223A224272697827746169656C6C65204869616C75222C227265616374696F6E5F6964223A31307D2C7B22757365725F6964223A33322C22757365726E616D65223A2247796527726F6E2056616C204F726964656E222C227265616374696F6E5F6964223A327D5D);