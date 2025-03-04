
## Relevant helidon MP v4 documentation

- [Persistence](https://helidon.io/docs/v4/mp/persistence)

## Hibernate tools

- Maven project for generating JPA classes from existing DB entities: https://github.com/hibernate/hibernate-tools/tree/main/maven

### Related commands

Describe plugin and goals

```bash
mvn help:describe -Dplugin=org.hibernate.tool:hibernate-tools-maven
```

Help on generating JPA entities from schema

```bash
mvn org.hibernate.tool:hibernate-tools-maven:help -Ddetail=true -Dgoal=hbm2java
```

Building persistence entities

```bash
mvn clean generate-sources
```

## TODOs

- Proper authentication schemes
- Robust filtering support
- Reasonable schemas implementation
- Reasonable service provider config
- Bulk api
- Fine tuning on EE / MP configuration for common concerns (logging etc...)
