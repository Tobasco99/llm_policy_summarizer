    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
    <soap:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soap:mustUnderstand="true">
        <wsse:UsernameToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="UsernameToken-1">
            <wsse:Username>n00f9vkm</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">Your received password</wsse:Password>
        </wsse:UsernameToken>
        </wsse:Security>
    </soap:Header>
    <soap:Body>
        <sear:searchRequest>
        <sear:expertQuery><![CDATA[Titel ~ 2021/535]]></sear:expertQuery>
        <sear:page>1</sear:page>
        <sear:pageSize>10</sear:pageSize>
        <sear:searchLanguage>de</sear:searchLanguage>
        </sear:searchRequest>
    </soap:Body>
    </soap:Envelope>